import numpy as np
import cv2

from .DeConvolve import DeConvolve
from ..config.constant import WIDTH
from ..config.constant import HEIGHT
from ..config.constant import SHOW_IMAGE

class Background:
  def __init__(self, video : cv2.VideoCapture):
    self.threshold = 500
    self.video = video
    # Khung hình ảnh
    self.frame = None

    self.kernel = np.ones((5, 5), np.uint8)
    self.min_area = 750

    self.__deconvolve = DeConvolve()

  def preprocessing(self, default = True, frame = None):
    # Tiến hành lọc nhiễu ảnh
    if default:
      __, frame = self.video.read()
    frame = cv2.resize(frame, (HEIGHT, WIDTH))

    # cv2.imshow("ORIGINAL", frame)

    # Lọc nhiễu + Chuyển đổi kênh màu
    init = cv2.medianBlur(frame, 7)
    init = cv2.bilateralFilter(init, 17, 27, 23)
    
    # cv2.imshow("FILTERED", init)

    init = cv2.cvtColor(init, cv2.COLOR_BGR2GRAY)
    
    return init, frame

  def run(self, bg = None):
    filtered_frame, frame = None, None
    if isinstance(bg, np.ndarray) == False:
      print("ok")
      filtered_frame, frame = self.preprocessing()
    else:
      filtered_frame, frame = self.preprocessing(frame=bg, default=False)

    if isinstance(self.frame, np.ndarray) == False:
      self.frame = filtered_frame

    if SHOW_IMAGE: cv2.imshow("BACKGROUND", self.frame)

    # So sánh nền
    mask = cv2.absdiff(self.frame, filtered_frame)

    # cv2.imshow("ABSDIFF", mask)

    # Thuật toán phát hiện cạnh làm rõ nét đối tượng
    mask = cv2.Canny(mask, 50, 200)

    if SHOW_IMAGE:
      cv2.imshow("CANNY", mask)

    # Thuật toán này góp phần làm dày cạnh
    mask = cv2.dilate(mask, self.kernel, iterations=2)
    
    contours, __ = cv2.findContours(mask,
      cv2.RETR_TREE,
      cv2.CHAIN_APPROX_SIMPLE
    )

    res = []
    for contour in contours:
      area = cv2.contourArea(contour)
      if area > self.min_area:
        res.append(cv2.boundingRect(contour))

    res = self.__deconvolve.run(res)
    return res, frame
  
  def from_path(self, path):
    img = cv2.imread(path)
    return self.run(bg=img)

  def add_background(self):
    ''' Gọi hàm này để tiến hành update ảnh background '''
    filtered_frame, frame = self.preprocessing()
    self.frame = filtered_frame
    return frame