import serial
import threading

from src.utils.standard_serial import standard
from src.config.essemble_code import SPLIT_PACKAGE
from src.config.essemble_code import NO_BARRIER

from ..internet.MaintainConnectionServer import MaintainConnectionServer

class Essemble:
  def __init__(self, arduino : serial.Serial, maintain : MaintainConnectionServer):
    self.arduino = arduino
    self.maintain = maintain
    
    self.__end_service = False

    # Some needed information
    # Biến này khi gửi gói tin thì sẽ có phản hồi
    self.response = False
    # Vật cản
    self.barriers = [NO_BARRIER] * 3

    # Nhận dữ liệu từ arduino
    threading.Thread(name="Arduino service", target=self.__arduino) \
      .start()

  def __arduino(self):
    print("Arduino service started")
    while not self.__end_service:
      commands = self.arduino.readline().decode("utf-8")
      commands = standard(commands)
      commands = commands.split(SPLIT_PACKAGE)

  def end(self):
    self.__end_service = True