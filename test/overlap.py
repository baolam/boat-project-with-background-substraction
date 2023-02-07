import cv2
import sys
import time

sys.path.append("./")

from src.image.Background import Background
from src.image.DeConvolve import DeConvolve

video = cv2.VideoCapture("./src/image/experiment/ocean.mp4")
# video = cv2.VideoCapture(0)
background = Background(video)
deconvle = DeConvolve()

for i in range(0, 5):
  video.read()

while True:
  rectangles, frame = background.run()
  print(rectangles)
  for rectangle in rectangles:
    x, y, w, h = rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
  cv2.imshow("IMAGE", frame)
  key = cv2.waitKey(1)
  if key == ord('q'):
    break
  if key == ord('u'):
    background.add_background()