import numpy as np
import serial
import cv2
import socketio
import threading
import requests
import time

from src.config.constant import WIDTH
from src.config.constant import HEIGHT
from src.config.constant import SERVER
from src.config.constant import IMAGE_API
from src.config.constant import NAMESPACE
from src.config.constant import SPLIT_PACKAGE
from src.config.constant import END_OF_PACKAGE
from src.config.constant import LEFT
from src.config.constant import RIGHT

from src.brain.Background import Background
from src.essemble.Essemble import Essemble
from src.utils.centroid import centroid
from src.utils.angle import angle

client = socketio.Client()
video = cv2.VideoCapture(0)
arduino = serial.Serial("COM10")
essemble = Essemble(arduino, client)
different = Background(video)

track_state = False
def track_garbage():
  global track_state
  track_state = True

def update_background():
  frame = different.add_background()
  file_name = '{}.png'.format(time.time())
  cv2.imwrite(file_name, frame)
  resp_code = requests.post(SERVER + IMAGE_API, files={
    "background" : open(file_name, "rb")
  })
  client.emit("notification", data={
    "status_code" : resp_code.status_code,
    "time" : essemble.time(),
    "text" : "Update background successfully"
  })

def socket_service():
  client.on("TRACK_GARBAGE", handler=track_garbage, namespace=NAMESPACE)
  client.on("UPDATE_BACKGROUND", handler=update_background, namespace=NAMESPACE)
  client.connect(SERVER, namespaces=[NAMESPACE])

threading.Thread(name="Socket service", target=socket_service) \
  .start()

try:
  while True:
    contour, frame = different.run()
    x, y, w, h = cv2.boundingRect(contour)
    centroid_point = centroid(x, y, w, h)
    deg, state = angle(centroid_point, WIDTH, HEIGHT)
    if track_state:
      code = RIGHT
      if not state: code = LEFT
      deg = int(deg)
      essemble.send_command(code + SPLIT_PACKAGE + deg + SPLIT_PACKAGE + END_OF_PACKAGE)
      client.emit("notification", data={
        "time" : Essemble.time(),
        "text" : "Tracking garbage"
      }, namespace=NAMESPACE)
      track_state = False
except:
  essemble.maintain = False
