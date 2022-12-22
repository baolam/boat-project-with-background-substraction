### Nguyên tắc là thiết bị trạm sẽ luôn có wifi
SERVER = ""
NAMESPACE = ""
HEALTH = "HEALTH"

import serial
import socketio
import threading

client = socketio.Client()
lora = serial.Serial()

def control_handler(command):
  print(command)

def client_service():
  client.on("control", handler=control_handler, namespace=NAMESPACE)
  try:
    client.connect(SERVER, namespaces=[NAMESPACE])
  except:
    pass

threading.Thread(name="Client service", target=client_service).start()
while True:
  commands = lora.readline().decode("utf-8") \
    .replace('\r\n', '')
  commands = commands.split(';')
  if commands[0] == HEALTH:
    lora.write(b'1;okok')