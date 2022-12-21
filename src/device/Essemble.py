import serial
import threading

from ..utils.standard_serial import standard
from ..config.essemble_code import SPLIT_PACKAGE
from ..config.essemble_code import NO_BARRIER
from ..config.essemble_code import SEND_DATA
from ..config.essemble_code import BARRIER_CODE
from ..config.essemble_code import RESPONSE_CONTROL

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
    
    self.ntu = 0
    self.tds = 0
    self.ph = 0
    self.c = 0

  def __arduino(self):
    print("Arduino service started")
    while not self.__end_service:
      commands = self.arduino.readline().decode("utf-8")
      commands = standard(commands)
      commands = commands.split(SPLIT_PACKAGE)

      if commands[0] == SEND_DATA:
        ntu, tds, ph = map(float, commands[1:])  
        self.ntu += ntu
        self.tds += tds
        self.ph += ph
        self.c += 1
      
      if commands[0] == BARRIER_CODE:
        self.barriers[0], self.barriers[1], self.barriers[2] = map(int, commands[1:])

      if commands[0] == RESPONSE_CONTROL:
        self.response = True
        
  def water_information(self):
    data = {
      "ntu" : self.ntu / self.c,
      "tds" : self.tds / self.c,
      "ph" : self.ph / self.c
    }
    self.ntu = 0
    self.tds = 0
    self.ph = 0
    self.c = 0
    return data
    
  def end(self):
    self.__end_service = True