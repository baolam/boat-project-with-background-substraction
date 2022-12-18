from src.internet.MaintainConnectionServer import MaintainConnectionServer

main = MaintainConnectionServer()
try:
  main.start()
except KeyboardInterrupt as e:
  main.telegram_service.stop()