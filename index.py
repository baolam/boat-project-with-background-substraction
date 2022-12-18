import cv2
import serial

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