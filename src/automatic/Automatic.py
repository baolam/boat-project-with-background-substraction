import serial
import time
import threading

from typing import List
from typing import Tuple
from mpu6050 import mpu6050

from ..config.automatic_code import ALL_LAKE
from ..config.automatic_code import ONLY_LAKESIDE
from ..config.automatic_code import NOT_WORKING
from ..config.automatic_code import DEFAULT_SPEED_MOTOR
from ..config.automatic_code import DEFAULT_ANGLE
from ..config.automatic_code import FORWARD
from ..config.automatic_code import LEFT
from ..config.automatic_code import RIGHT
from ..config.automatic_code import SPECIFIC_HANDLE
from ..config.automatic_code import STOP

from ..config.essemble_code import NO_BARRIER
from ..config.essemble_code import HAS_BARRIER
from ..config.essemble_code import SPLIT_PACKAGE
from ..config.essemble_code import END_PACKAGE
from ..device.Essemble import Essemble

from .MatrixPoint import MatrixPoint
from .TraceData import TraceData
from .statergy import only_lake

class Robot:
  def __init__(self, device : serial.Serial):
    self.device = device
    self.percentage = DEFAULT_SPEED_MOTOR
    self.angle = DEFAULT_ANGLE
  
  def write(self, data):
    self.write_signal(data, self.device)

  @staticmethod
  def write_signal(data, device):
    device.write(b'{}'.format(data))

  def forward(self):
    self.write(FORWARD + SPLIT_PACKAGE + str(self.percentage) + SPLIT_PACKAGE + str(self.percentage) 
    + SPLIT_PACKAGE + END_PACKAGE)

  def left(self, angle = None):
    if angle == None:
      angle = self.angle
    self.write(LEFT + SPLIT_PACKAGE + str(angle) + SPLIT_PACKAGE + END_PACKAGE)

  def right(self, angle = None):
    if angle == None:
      angle = self.angle
    self.write(RIGHT + SPLIT_PACKAGE + str(angle) + SPLIT_PACKAGE + END_PACKAGE)

  def stop(self):
    self.write(STOP + SPLIT_PACKAGE + END_PACKAGE)

sensor = mpu6050(0x68)
class Automatic:
  def __init__(self, essemble : Essemble, maintain):
    self.mode = NOT_WORKING 
    self.essemble = essemble
    self.robot = Robot(essemble.arduino)
    self.mp = MatrixPoint()
    self.trace_data = TraceData(maintain)

    self.__end_service = False
    self.speed = 0
    
    # Cac thong so cua thiet bi do mpu6050
    self.alpha = 0.2
    # Gia tri loi cua cam bien gia toc
    self.theta = 0.6
    self.a0 = 0
    self.v0 = 0
    # Tín hiệu từ mpu
    threading.Thread(name="MPU6050 service", target=self.__mpu6050) \
      .start()
    
  def update_mode(self, mode):
    self.mode = mode
  
  def update_background(self, rectangles, frame):
    self.rectangles = rectangles
    self.frame = frame

  def run(self, trash_areas : List[
    Tuple[int, int, int, int]], frame
  ):
    if self.mode == NOT_WORKING:
      return
    if self.mode == ONLY_LAKESIDE:
      self.only_lakeside()
    if self.mode == ALL_LAKE:
      self.all_lake_mode(trash_areas, frame)

  def all_lake_mode(self):
    print("Run on all_lake mode")
    pass
    
  def only_lakeside(self):
    print("Run on only lakeside")
    if self.mp.x == 0 and self.mp.y == 0:
      code = only_lake(self.essemble.barriers)
    if code == SPECIFIC_HANDLE:
      self.robot.stop()
      __, forward, right = self.essemble.barriers
      if forward == HAS_BARRIER and right == HAS_BARRIER:
        self.__turn_escape_curve()
      elif forward == HAS_BARRIER:
        self.__turn_escape_curve()
      elif right == NO_BARRIER:
        self.__track_barrier()
    elif code == FORWARD:
      self.robot.forward()
    self.trace()
    self.mode = NOT_WORKING
    self.trace_data.send_data()

  def trace(self):
    self.trace_data.add_data(self.essemble.water_information(), -1, 
      self.mp.coordinate(), self.boat_information())

  def __turn_escape_curve(self):
    codes = [ LEFT, FORWARD, RIGHT ]
    self.__compile(codes)

  def __compile(self, codes):
    for code in codes:
      self.essemble.response = False
      if code == LEFT: self.robot.left(20)
      elif code == FORWARD: self.robot.forward()
      elif code == RIGHT: self.robot.right(20)
      while not self.essemble.response:
        pass

  def __track_barrier(self):
    codes = [ RIGHT, FORWARD, LEFT ]
    self.__compile(codes)

  # Phương thức này là lắng nghe thay đổi của thuyền (về vận tốc -> quãng đường)
  def __mpu6050(self):
    # I suppose it's ok
    # https://pypi.org/project/mpu6050-raspberrypi/
    # https://www.youtube.com/watch?v=JTFa5l7zAA4
    # https://microdigisoft.com/mpu6050-accelerometergyroscope-sensor-interfacing-with-raspberry-pi/
    # https://pypi.org/project/mpu6050-raspberrypi/
    # https://electronics.stackexchange.com/questions/142037/calculating-angles-from-mpu6050

    print("MPU6050 service started")
    while not self.__end_service:
      pTime = time.time()
      a = sensor.get_accel_data()["x"]
      a -= self.theta
      a = a * self.alpha + (1 - self.alpha) * self.a0
      cTime = time.time()
      self.speed = self.v0 + a * ((cTime - pTime) / 1000)
      self.a0 = a
      self.v0 = self.speed
      self.mp.run(self.speed * 0.001)

  def boat_information(self):
    return {
      "speed" : self.speed
    }