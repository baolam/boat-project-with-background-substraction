import serial
import threading
import socketio
import datetime

from ..config.constant import SPLIT_PACKAGE
from ..config.constant import END_OF_PACKAGE
from ..config.constant import SEND_DATA
from ..config.constant import ASK_RECEVIER
from ..config.constant import ANSWER
from ..config.constant import NAMESPACE
from ..config.constant import RECORD
from ..config.constant import LEFT
from ..config.constant import RIGHT
from ..config.constant import FORWARD
from ..config.constant import RESPONSE_CONTROL
from ..config.constant import BARRIER_CODE
from ..config.constant import FORWARD
from ..config.constant import NAMESPACE

class Essemble:
    def __init__(self, arduino: serial.Serial, socket: socketio.Client):
        self.arduino = arduino
        self.socket = socket
        self.socket_ok = False
        self.maintain = True
        self.barriers = [0] * 3
        self.barrier_commands = [LEFT, FORWARD, RIGHT]

        # Viết module để đo tốc độ :>
        # Tốc độ là 4.16 m/s
        self.speed = 4.16
        # Phần trăm tốc độ động cơ
        self.percentage_speed = 50
        # Khoảng thời gian lấy mẫu
        self.delta = 0.1
        
        threading.Thread(name="Essemble_device", target=self.__read_command) \
            .start()

        self.socket.on("control", handler=self.control_event, namespace=NAMESPACE)
        self.socket.on("UPDATE_SPEED", handler=self.update_speed_event, namespace=NAMESPACE)

    def control_event(self, code):
        if code == FORWARD:
            self.send_command(code + SPLIT_PACKAGE + str(self.percentage_speed) + SPLIT_PACKAGE + str(self.percentage_speed) 
                + SPLIT_PACKAGE + END_OF_PACKAGE)
        elif code == LEFT or code == RIGHT:
            self.send_command(code + SPLIT_PACKAGE + str(90) + SPLIT_PACKAGE + END_OF_PACKAGE)
        else:
            self.send_command(code + END_OF_PACKAGE)

    def update_speed_event(self, speed):
        self.percentage_speed = speed
        self.socket.emit("notification", data={
            "time" : self.time(),
            "tẽtx" : "Update speed successfully"
        })

    @staticmethod
    def time():
        time = datetime.datetime.now()
        return '{}:{}:{}'.format(time.hour, time.minute, time.second)

    def __send_command(self, command):
        command = bytes(command, "utf-8")
        self.arduino.write(command)
    
    def send_command(self, command):
        self.__send_command(command)

    def __read_command(self):
        while self.maintain:
            commands = self.arduino.readline()
            commands = commands.decode("utf-8") \
                .replace('\r', '').replace('\n', '')

            commands = commands.split(END_OF_PACKAGE)[0]
            commands = commands.split(SPLIT_PACKAGE)
            
            print("Dữ liệu nhận được từ Arduino ", commands)

            if commands[0] == SEND_DATA:
                ntu = float(commands[1])
                tds = float(commands[2])

                # Gửi dữ liệu lên server
                self.socket.emit(RECORD, {
                    "ntu": ntu, "tds": tds
                }, namespace=NAMESPACE)

            if commands[0] == ASK_RECEVIER:
                print("Arduino đã hoạt động")
                self.__send_command(ANSWER + END_OF_PACKAGE)
                self.__send_command('S#')
                if self.socket.connected:
                    self.socket.emit("notification", data={
                        "time" : self.time(),
                        "text" : "Arduino worked"
                    })

            if commands[0] == RESPONSE_CONTROL:
                distance = self.speed * self.delta
                temp = int(commands[2])
                if commands[1] == FORWARD:
                    self.percentage_speed = temp
                package = {
                    "distance" : distance,
                    "angle" : 0,
                    "speed" : self.percentage_speed,
                    "code" : commands[1]
                }
                if commands[1] != FORWARD:
                    package["angle"] = temp
                self.socket.emit("POSITION", data=package)
                
            if commands[0] == BARRIER_CODE:
                for i in range(1, 4):
                    self.barriers[i - 1] = int(commands[i])
                text = 'Barriers_state'
                
                for i in range(0, 3):
                    if self.barriers[i]:
                        text = text + self.barrier_commands[i] + ';'

                self.socket.emit("notification", data={
                    "time" : self.time(),
                    "text" : text
                })

            # Các sự kiện liên quan đến duy trì socket và thông báo
            if not self.socket_ok and self.socket.connected:
                self.socket_ok = True
                self.socket.emit("notification", data={
                    "time" : self.time(),
                    "text" : "Raspberry pi worked"
                })

            if self.socket.connected == False:
                self.socket_ok = False
