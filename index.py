import cv2
import serial
import threading

from src.image.Background import Background
from src.device.Essemble import Essemble
from src.device.LoraSignal import LoraSignal
from src.internet.MaintainConnectionServer import MaintainConnectionServer
from src.automatic.Automatic import Automatic

arduino = serial.Serial()
lora = serial.Serial()
video = cv2.VideoCapture(0)

maintain = MaintainConnectionServer()
background = Background(video)

essemble = Essemble(arduino, maintain)
automatic = Automatic(essemble)
lorasignal = LoraSignal(lora, automatic)

# Thêm các sự kiện server
maintain.add_handler("mode", automatic.update_mode)
maintain.start()

# I merge you this line
stop = False
try:
  def _background():
    global stop
    while not stop:
      rectangles, frame = background.run()
      automatic.update_background(rectangles, frame)
    
  threading.Thread(name = "Background service", target = _background) \
    .start()
  maintain.start()
except:
  essemble.end()
  lorasignal.end()
  stop = True