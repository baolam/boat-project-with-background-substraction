import serial
import threading

from typing import List
from typing import Tuple

from src.config.automatic_code import ALL_LAKE
from src.config.automatic_code import ONLY_LAKESIDE
from src.config.automatic_code import DEFAULT_SPEED_MOTOR
from src.config.automatic_code import DEFAULT_ANGLE
from src.config.automatic_code import FORWARD
from src.config.automatic_code import LEFT
from src.config.automatic_code import RIGHT

from src.config.essemble_code import SPLIT_PACKAGE
from src.config.essemble_code import END_PACKAGE
from ..device.Essemble import Essemble

from .MatrixPoint import MatrixPoint

class Robot:
  def __init__(self, device : serial.Serial):
    self.device = device
    self.percentage = DEFAULT_SPEED_MOTOR
    self.angle = DEFAULT_ANGLE
  
  def write(self, data):
    self.device.write(b'{}'.format(data))

  def forward(self):
    self.write(FORWARD + SPLIT_PACKAGE + str(self.percentage) + SPLIT_PACKAGE + str(self.percentage) 
    + SPLIT_PACKAGE + END_PACKAGE)

  def left(self, angle = None):
    if angle == None:
      angle = self.angle
    self.write(LEFT + SPLIT_PACKAGE + str(angle) + SPLIT_PACKAGE + END_PACKAGE)

  def right(self, angle):
    if angle == None:
      angle = self.angle
    self.write(RIGHT + SPLIT_PACKAGE + str(angle) + SPLIT_PACKAGE + END_PACKAGE)

class Automatic:
  def __init__(self, essemble : Essemble):
    self.mode = ONLY_LAKESIDE
    self.essemble = essemble
    self.robot = Robot(essemble.arduino)
    self.mp = MatrixPoint()

    self.__end_service = False
    # Tín hiệu từ mpu
    threading.Thread(name="MPU6050 service", target=self.__mpu6050) \
      .start()

  def update_mode(self, mode):
    self.mode = mode
  
  def run(self, trash_areas : List[
    Tuple[int, int, int, int]]
  ):
    if self.mode == ONLY_LAKESIDE:
      self.only_lakeside()
    if self.mode == ALL_LAKE:
      self.all_lake_mode(trash_areas)

  def all_lake_mode(self, trash_areas):
    print("Run on all_lake mode")
    
  def only_lakeside(self):
    print("Run on only lakeside")
  
  # Phương thức này là lắng nghe thay đổi của thuyền (về vận tốc -> quãng đường)
  def __mpu6050(self):
    # I suppose it's ok
    # https://pypi.org/project/mpu6050-raspberrypi/
    # https://www.youtube.com/watch?v=JTFa5l7zAA4

    print("MPU6050 service started")
    while not self.__end_service:
      pass 