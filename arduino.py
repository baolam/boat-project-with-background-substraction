import serial
import socketio
import threading
from src.essemble.Essemble import Essemble

client = socketio.Client()
arduino = serial.Serial("COM5")

def service_socket():
  client.connect("http://noise-detector.herokuapp.com", namespaces=["/"])

essemble = Essemble(arduino, client)
threading.Thread(name="Io service", target=service_socket) \
  .start()
try:
  while True:
    command = input()
    essemble.send_command(command)
except:
  essemble.maintain = False