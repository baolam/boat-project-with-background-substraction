import sys
import os

sys.path.append("./")

import cv2
from src.image.Background import Background

video = cv2.VideoCapture(0)
bg = Background(video)

def get_path(path):
  return './background/trash/{}.jpg'.format(path )

# ls = ["2", "3", "4", "5", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "29", "30", "35",]
ls = [obj.split('.')[0] for obj in os.listdir("./background/trash")]

i = 0
bg.from_path('./background/bg/6.jpg')
while True:
  rectangles, frame = bg.from_path(get_path(ls[i])) 
  # print(rectangles)
  for rectangle in rectangles:
    x, y, w, h = rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
  cv2.imshow("IMAGE", frame)
  key = cv2.waitKey(1)
  if key == ord('q'):
    break
  if key == ord('n'):
    i += 1
    if len(ls) == i:
      break