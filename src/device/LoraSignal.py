import serial
import threading

from src.utils.standard_serial import standard

from src.config.essemble_code import SPLIT_PACKAGE
from src.config.automatic_code import HAND_CONTROL
from src.config.automatic_code import FORWARD
from src.config.automatic_code import LEFT
from src.config.automatic_code import RIGHT
from src.automatic.Automatic import Automatic

class LoraSignal:
  def __init__(self, lora : serial.Serial, auto : Automatic):
    self.lora = lora
    self.robot = auto.robot
    self.__end_service = False

    threading.Thread(name="Lora service", target=self.__service) \
      .start()

  def __service(self):
    print ("Start lora service")
    while not self.__end_service:
      commands = self.lora.readline()
      commands = standard(commands.decode('utf-8'))
      commands = commands.split(SPLIT_PACKAGE)
      print(commands)
      if len(commands) > 0 and commands[0] == HAND_CONTROL:
          code = commands[1]
          if code == FORWARD: self.robot.forward()
          if code == LEFT: self.robot.left()
          if code == RIGHT: self.robot.right()

  def end(self):
    self.__end_service = True