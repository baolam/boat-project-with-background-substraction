import numpy as np
import cv2
import os
import time

from ..config.constant import WIDTH
from ..config.constant import HEIGHT

class Background:
  def __init__(self, video : cv2.VideoCapture):
    self.threshold = 500
    self.video = video
    # Khung hình ảnh
    self.frame = None

    self.kernel = np.ones((5, 5), np.uint8)
    self.background_substractor = cv2.createBackgroundSubtractorMOG2()
  
  def preprocessing(self):
    # Tiến hành lọc nhiễu ảnh
    __, frame = self.video.read()
    frame = cv2.resize(frame, (HEIGHT, WIDTH))
    init = cv2.medianBlur(frame, 13)
    return init, frame

  def run(self):
    filtered_frame, frame = self.preprocessing()
    if isinstance(self.frame, np.ndarray) == False:
      self.frame = filtered_frame

    mask = self.background_substractor.apply(filtered_frame)
    mask = cv2.dilate(mask, self.kernel)

    contours, __ = cv2.findContours(mask,
                                           cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)
    max_contour = 0
    result_contour = None
    for __, contour in enumerate(contours):
      area = cv2.contourArea(contour)
      if area > self.threshold and max_contour < area:
        max_contour = area
        result_contour = contour
    
    return result_contour, frame
  
  def add_background(self):
    ''' Gọi hàm này để tiến hành update ảnh background '''
    filtered_frame, frame = self.preprocessing()
    self.frame = filtered_frame
    return frame