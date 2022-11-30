import cv2
import numpy as np

from typing import Tuple
from typing import Any
from ..config.constant import WIDTH
from ..config.constant import HEIGHT

class FlagPosition:
  def __init__(self, lower, upper, video : cv2.VideoCapture, threshold : int = 700):
    self.lower = lower
    self.upper = upper
    self.video = video
    self.threshold = threshold
    self.kernal = np.ones((5, 5), "uint8")

  def identify(self) -> Tuple[Any, Any]:
    __, frame = self.video.read()
    frame = cv2.resize(frame, (HEIGHT, WIDTH))
    # Loại bỏ nhiễu muối tiêu
    __frame = cv2.medianBlur(frame, 17)

    # print(cv2.cvtColor(__frame, cv2.COLOR_BGR2HSV))
    mask = cv2.inRange(cv2.cvtColor(__frame, cv2.COLOR_BGR2HSV), self.lower, self.upper)
    mask = cv2.dilate(mask, self.kernal)
    # res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow("FLAG_POSITION", res)
    contours, __ = cv2.findContours(mask,
                                           cv2.RETR_TREE,
                                          cv2.CHAIN_APPROX_SIMPLE)
    max_contour = 0
    result_contour = None
    for __, contour in enumerate(contours):
      area = cv2.contourArea(contour)
      if area > self.threshold:
        # x, y, w, h = cv2.boundingRect(contour)
        # frame = cv2.rectangle(frame, (x, y), 
        #                             (x + w, y + h), 
        #                             (0, 0, 255), 2)
        if max_contour < area:
          max_contour = area
          result_contour = contour
    
    # cv2.imshow("REAL_IMAGE", frame)
    return result_contour, frame