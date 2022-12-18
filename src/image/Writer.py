import cv2
import time

from src.config.constant import HEIGHT
from src.config.constant import WIDTH
from src.config.constant import SAVED_VIDEO

# https://viblo.asia/p/opencv-with-python-part-2-L4x5xRRBZBM
# https://www.tutorialspoint.com/python/time_time.htm

class Writer:
  def __init__(self):
    self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
    self.end_of_vid = 90 # Kết thúc trong 90s

  def write(self, frame):
    self.video.write(frame)
    delta = time.time() - self.initalize

    seconds = int(delta % 60)
    minutes = int(delta / 60) 
    time_delta = minutes * 60 + seconds
    
    if time_delta >= self.end_of_vid:
      self.video.release()
      return True
    return False
  
  def update_end_vid(self, time_second):
    self.end_of_vid = time_second * 3
  
  def create_writer(self, file_name):
    self.video = cv2.VideoWriter('{}/{}.avi'.format(SAVED_VIDEO, file_name), 
      self.fourcc, 20, (HEIGHT, WIDTH)
    )
    self.initalize = time.time()
    