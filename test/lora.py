import sys
import threading

sys.path.append("./")

import serial
from src.device.LoraSignal import LoraSignal
from src.automatic.Automatic import Robot, Automatic
from src.device.Essemble import Essemble

stop = False
lora = serial.Serial("COM5", 9600, parity=serial.PARITY_NONE, 
  stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

def receive_data():
  global stop
  while not stop:
    r = lora.readline().decode("utf-8").replace("\r\n", '')
    if len(r) > 0:
      print(r)

threading.Thread(name = "Lora service", target = receive_data).start()

try:
  while True:
    command = input("Đầu vào: ")
    Robot.write_signal(command, lora)
except KeyboardInterrupt as e:
  stop = True