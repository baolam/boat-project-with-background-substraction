print("Import thư viện")
import numpy as np
import cv2

from src.config.constant import WIDTH
from src.config.constant import HEIGHT
from src.brain.Flag import FlagPosition
from src.position import angle
print("Import hoàn tất")

video = cv2.VideoCapture(0)
print("Video hoàn tất")
flag = FlagPosition(
  np.array([22, 93, 0], np.uint8), 
  np.array([45, 255, 255], np.uint8), 
video)
print("Flag hoàn tất")

while True:
  contour, frame = flag.identify()
  x, y, w, h = cv2.boundingRect(contour)
  frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
  frame = cv2.circle(frame, (x + w // 2, y + h // 2), 3, (0, 255, 0), 2)
  cv2.imshow("REAL_IMAGE", frame)
  print(angle((x + w // 2, y + h // 2), WIDTH, HEIGHT))
  if cv2.waitKey(10) & 0xFF == ord('q'):
    break