import socketio
import threading
import time
import os

from ..config.constant import SERVER
from ..config.constant import NAMESPACE
from ..config.constant import TOKEN_TELEGRAM
from ..config.constant import CHANNEL_ID
from ..config.essemble_code import SPLIT_PACKAGE

from ..config.socket_code import UPDATE_HOST
from ..config.socket_code import DEFAULT_SSID
from ..config.socket_code import DEFAULT_PASSWORD
from ..config.socket_code import ASK_WIFI
from ..config.socket_code import UPDATE_WIFI

from telegram import Bot
from telegram.ext import MessageHandler, Updater, Filters
from telegram.utils.request import Request

from .Internet import Internet

class MaintainConnectionServer:
  ROOT_PATH = "src/internet/storage"

  def __init__(self):
    self.client = socketio.Client()
    self.my_server = SERVER
    self.internet = Internet(DEFAULT_SSID, DEFAULT_SSID, DEFAULT_PASSWORD)

    # Khởi tạo bot
    request = Request()
    self.bot = Bot(TOKEN_TELEGRAM, request=request)

  def start(self):
    self.__client_srv()
    self.__initalize_bot()

  def __client_srv(self):
    threading.Thread(name = "Client service", target=self.__client) \
      .start()

  def __client(self):
    print("Client service")
    try:
      self.client.connect(self.my_server, namespaces=[NAMESPACE])
    except Exception as e:
      self.__error_server(e)

  def add_handler(self, event, callback):
    self.client.on(event, handler=callback, namespace=NAMESPACE)
  
  def __message(self, message_obj, __):
    message = message_obj.message.text
    message = message.split(SPLIT_PACKAGE)
    if message[0] == UPDATE_HOST:
      self.__update_host(message)
    if message[0] == ASK_WIFI:
      self.__ask_wifi()
    if message[0] == UPDATE_WIFI:
      self.__update_wifi(message)

  def __initalize_bot(self):
    print("Initalize bot")
    try:
      updater = Updater(bot = self.bot, use_context = True)
      dp = updater.dispatcher
      dp.add_handler(MessageHandler(Filters.all, self.__message))
      self.telegram_service = updater
      updater.start_polling()
      updater.idle()
    except KeyboardInterrupt as e:
      print(e)
  
  def __reconnect_socket(self):
    if self.client.connected:
      self.client.disconnect()
    self.client_srv()

  def __error_server(self, err):
    file_name = "{}/{}.txt".format(self.ROOT_PATH, time.time())
    with open(file_name, "w", encoding = "utf-8") as fout:
      fout.write(str(err))
    self.bot.send_message(CHANNEL_ID, text = "Lỗi kết nối tới server")
    with open(file_name, "rb") as fin:
      self.bot.send_document(CHANNEL_ID, fin)
    os.remove(file_name)

  def __update_host(self, message):
    self.my_server = message[1]
    self.bot.send_message(CHANNEL_ID, text = "Đã cập nhật máy chủ thành công")
    self.__reconnect_socket()
  
  def __ask_wifi(self):
    has_internet = Internet.internet_connection()
    if has_internet:
      self.bot.send_message(CHANNEL_ID, text = "Có wifi")
    
  def __update_wifi(self, message):
    if len(message) != 3:
      self.bot.send_message(CHANNEL_ID, text = "Yêu cầu cập nhật wifi bị từ chối")
      return
    __, ssid, password = message
    self.internet = Internet(ssid, ssid, password)
    self.internet.run()