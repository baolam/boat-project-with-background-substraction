import sys
import cv2
import numpy as np

sys.path.append('./')

from src.image.DeConvolve import DeConvolve
from src.config.constant import HEIGHT
from src.config.constant import WIDTH

data = [(237, 463, 52, 49), (108, 414, 86, 98), (322, 397, 145, 115), (202, 385, 33, 115), (34, 349, 57, 163), (155, 75, 212, 331)]
convolve = DeConvolve()

img = np.zeros((HEIGHT + 100, WIDTH + 100, 3))
img2 = np.zeros((HEIGHT + 100, WIDTH + 100, 3))
for x, y, w, h in data:
  cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
z = convolve.run(data)
for x, y, w, h in z:
  cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 1)
while True:
  cv2.imshow("BEFORE", img)
  cv2.imshow("AFTER", img2)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
