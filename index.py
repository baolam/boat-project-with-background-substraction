### Nguyên tắc là thiết bị trạm sẽ luôn có wifi
server = ""
NAMESPACE = ""
HEALTH = "HEALTH"

import serial
import socketio
import threading
from telegram import Bot
from telegram.ext import MessageHandler, Updater, Filters
from telegram.utils.request import Request

update_server = False
def receive(message, __):
  global update_server
  print(message.message)
  update_server = True

TOKEN_TELEGRAM = "5843674768:AAFKqehrPbVVwOC29i6Qm-TYo2rRfabNZEw"
request = Request()
bot = Bot(token = TOKEN_TELEGRAM, request = request)
updater = Updater(bot=bot, use_context = True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(filters=Filters.all, callback=receive))

barrier_code = "BARRIER_CODE"
send_data = "SEND_DATA"
response_control = "R"

client = socketio.Client()
lora = serial.Serial("/dev/ttyUSB0")

def control_handler(command):
  lora.write(bytes('HAND_CONTROL;{};#'.format(command), "utf-8"))
  client.emit("RESPONSE", {
    "code" : "HAND_CONTROL",
    "response" : command
  })

def client_service():
  global update_server
  client.on("control", handler=control_handler, namespace=NAMESPACE)
  try:
    while not update_server:
      pass
    client.connect(server, namespaces=[NAMESPACE])
  except KeyboardInterrupt as e:
    client.disconnect()

def telegram_service():
  updater.start_polling()
  updater.idle()

def lora_service():
  while True:
    commands = lora.readline().decode("utf-8") \
      .replace('\r\n', '')
    commands = commands.split(';')
    if commands[0] == HEALTH:
      lora.write(b'1;okok')
    if commands[0] == send_data:
        ntu, tds, ph = map(int, commands[1:])
        client.emit("record", data={
            "ntu" : ntu, "tds" : tds, "ph" : ph
        }, namespace = NAMESPACE)
    if commands[0] == barrier_code:
        left, forward, right = map(bool, commands[1:])
        client.emit("barrier_code", data={
          "left" : left, "right" : right, "forward" : forward
        }, namespace=NAMESPACE)
    
threading.Thread(name="Client service", target=client_service).start()
threading.Thread(name="Lora service", target=lora_service).start()
telegram_service()