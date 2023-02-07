import sys

sys.path.append("./")

import serial
from src.device.Essemble import Essemble
from src.device.LoraSignal import LoraSignal
from src.internet.MaintainConnectionServer import MaintainConnectionServer
from src.automatic.Automatic import Robot

maintain = MaintainConnectionServer()
lora = serial.Serial("COM5")
arduino = serial.Serial("COM4")

essemble = Essemble(arduino, maintain, lora)
while True:
  command = input("Nhập lệnh: ")
  Robot.write_signal(command, arduino)