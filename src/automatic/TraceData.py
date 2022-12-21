##### Lưu dữ liệu ####
# Lưu thông tin ntu, tds
# Lưu thông tin ảnh nhận dạng
# Lưu thông tin về tọa độ
import time
import cv2
import json
import base64
import os
import requests

from ..config.constant import SERVER
from ..config.constant import SEND_DATA

from ..internet.MaintainConnectionServer import MaintainConnectionServer
class TraceData:
  ROOT_PATH = "src/storage"
  def __init__(self, maintain : MaintainConnectionServer):
    self.maintain = maintain

  def name(self, file_name, tail):
    return '{}/{}.{}'.format(TraceData.ROOT_PATH, file_name, tail)

  def add_data(self, water_information, image, coordinate, boat_information):
    file_name = '{}'.format(time.time())
    save_file = self.name(file_name, "json")
    image = None
    
    if isinstance(image, int):
      image = -1
    else: image = self.__convert_image(file_name, image)
    
    object_data = {
      "water_information" : water_information,
      "image" : image,
      "coordinate" : coordinate,
      "boat_information" : boat_information
    }
    
    with open(save_file, "w", encoding = "utf-8") as fout:
      json.dump(object_data, fout, ensure_ascii = False)
    
    return save_file

  def __convert_image(self, file_name ,image):
    # https://appdividend.com/2022/09/15/how-to-convert-image-to-base64-string-in-python/
    save_file = self.name(file_name, "png")
    cv2.imwrite(save_file, image)
    with open(save_file, "rb") as fin:
      b64_string = base64.b64encode(fin.read())
    os.remove(save_file)
    return b64_string.decode("utf-8")

  def send_data(self):
    file_names = os.listdir(TraceData.ROOT_PATH)
    self.maintain.internet.connect()
    for file_name in file_names:
      with open('{}/{}'.format(TraceData.ROOT_PATH, file_name), "rb") as fin:
        requests.post(SERVER + SEND_DATA, files={
          "data" : fin.read()
        })
        