import serial
import threading

from ..utils.standard_serial import standard
from ..config.essemble_code import SPLIT_PACKAGE
from ..config.essemble_code import NO_BARRIER
from ..config.essemble_code import SEND_DATA
from ..config.essemble_code import BARRIER_CODE
from ..config.essemble_code import RESPONSE_CONTROL

from ..config.essemble_code import END_PACKAGE
from ..config.essemble_code import SPLIT_PACKAGE
from ..config.constant import ASK_RECEIVER
from ..config.constant import ANSWER

from ..internet.MaintainConnectionServer import MaintainConnectionServer
from ..automatic.Automatic import Robot

class Essemble:
  def __init__(self, arduino : serial.Serial, 
    maintain : MaintainConnectionServer, lora : serial.Serial):
    self.arduino = arduino
    self.maintain = maintain
    self.lora = lora
    
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
    self.c = 1

  def __arduino(self):
    print("Arduino service started")
    while not self.__end_service:
      commands = self.arduino.readline().decode("utf-8")
      commands = standard(commands)
      commands = commands.split(SPLIT_PACKAGE)

      # print("Received data from arduino ", commands)

      if commands[0] == SEND_DATA:
        ntu, tds, ph = map(float, commands[1:])  
        self.ntu += ntu
        self.tds += tds
        self.ph += ph
        self.c += 1
        # Robot.write_signal(SEND_DATA + SPLIT_PACKAGE + commands[1] + SPLIT_PACKAGE + commands[2] 
        #   + SPLIT_PACKAGE + commands[3] + SPLIT_PACKAGE + END_PACKAGE, self.lora)
      
      if commands[0] == BARRIER_CODE:
        self.barriers[0], self.barriers[1], self.barriers[2] = map(int, commands[1:])
        # Robot.write_signal(BARRIER_CODE + SPLIT_PACKAGE + commands[1] + SPLIT_PACKAGE + commands[2] 
        #   + SPLIT_PACKAGE + commands[3] + SPLIT_PACKAGE + END_PACKAGE, self.lora)

      if commands[0] == RESPONSE_CONTROL:
        self.response = True
        Robot.write_signal(RESPONSE_CONTROL + SPLIT_PACKAGE + commands[1] + 
          SPLIT_PACKAGE + END_PACKAGE, self.lora)
      
      if commands[0] == ASK_RECEIVER:
        Robot.write_signal(ANSWER + END_PACKAGE, self.arduino)
        Robot.write_signal(ANSWER + END_PACKAGE, self.lora)

  def water_information(self):
    data = {
      "ntu" : self.ntu / self.c,
      "tds" : self.tds / self.c,
      "ph" : self.ph / self.c
    }
    self.ntu = 0
    self.tds = 0
    self.ph = 0
    self.c = 1
    return data
    
  def end(self):
    self.__end_service = True