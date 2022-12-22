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

client = socketio.Client()
lora = serial.Serial("/dev/ttyAMA0")

def control_handler(command):
  print(command)

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

threading.Thread(name="Client service", target=client_service).start()
threading.Thread(name="Lora service", target=lora_service).start()
telegram_service()