import cv2
import serial
import threading
import sys

from src.image.Background import Background
from src.device.Essemble import Essemble
from src.device.LoraSignal import LoraSignal
from src.internet.MaintainConnectionServer import MaintainConnectionServer
from src.automatic.Automatic import Automatic

arduino = serial.Serial("COM4")
lora = serial.Serial("COM5")
video = cv2.VideoCapture(0)

maintain = MaintainConnectionServer()
background = Background(video)

essemble = Essemble(arduino, maintain, lora)
automatic = Automatic(essemble, maintain)
lorasignal = LoraSignal(lora, automatic)

# Thêm các sự kiện server
maintain.add_handler("mode", automatic.update_mode)

# I merge you this line
stop = False
try:
  def _background():
    global stop
    while not stop:
      rectangles, frame = background.run()
      for x, y, w, h in rectangles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
      automatic.update_background(rectangles, frame)
      # cv2.imshow("TEST", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
  threading.Thread(name = "Background service", target = _background) \
    .start()
  maintain.start()
except KeyboardInterrupt as e:
  print(e)
  sys.exit(0)