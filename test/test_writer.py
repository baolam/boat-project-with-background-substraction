import sys
import cv2

sys.path.append("./")

from src.automatic.TraceData import TraceData
trace = TraceData()
video = cv2.VideoCapture(0)

__, frame = video.read()
trace.add_data({
  "ntu" : -1,
  "tds" : -1,
  "ph" : -1
}, frame, {
  "x" : 0,
  "y" : 0
}, {
  "speed" : 10,
  "speed_angle" : 2,
  "percentage_speed" : 50
})