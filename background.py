import cv2

from src.config.constant import WIDTH
from src.config.constant import HEIGHT
from src.brain.Background import Background
from src.utils.centroid import centroid

video = cv2.VideoCapture(0)
background = Background(video)

while True:
  contour, frame = background.run()
  x, y, w, h = cv2.boundingRect(contour)
  frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
  frame = cv2.circle(frame, centroid(x, y, w, h), 3, (0, 255, 0), 2)
  cv2.imshow("REAL_IMAGE", frame)
  if cv2.waitKey(10) & 0xFF == ord('q'):
    break