import serial
import socketio

from ..essemble.Essemble import Essemble
from ..utils.angle import angle

from ..config.constant import TEST_TURN_LEFT_RIGHT
from ..config.constant import TEST_TURN_LEFT_RIGHT_IMAGE
from ..config.constant import NAMESPACE
from ..config.constant import LEFT
from ..config.constant import RIGHT
from ..config.constant import END_OF_PACKAGE
from ..config.constant import SPLIT_PACKAGE
from ..config.constant import WIDTH
from ..config.constant import HEIGHT


class Position(Essemble):
    def __init__(self, arduino: serial.Serial, socket: socketio.Client):
        super().__init__(arduino, socket)

        self.socket.on(TEST_TURN_LEFT_RIGHT,
                       handler=self.__turn_left_right, namespace=NAMESPACE)
        self.socket.on(TEST_TURN_LEFT_RIGHT_IMAGE,
                       handler=self.__turn_left_right_image, namespace=NAMESPACE)

    def __turn_left_right(self, command):
        left = command["is_left"]
        _angle = command["angle"]

        code = LEFT
        if not left:
            code = RIGHT

        _angle = int(_angle)
        self.__send_command(code + SPLIT_PACKAGE + _angle +
                            SPLIT_PACKAGE + END_OF_PACKAGE)
        self.socket.emit("position", data={
            "code" : code,
            "angle" : _angle
        })

    def __turn_left_right_image(self, command):
        centroid = (command["x"], command["y"])
        _angle, left = angle(centroid, WIDTH, HEIGHT)
        code = LEFT
        if not left:
            code = RIGHT
        _angle = int(_angle)
        self.__send_command(code + SPLIT_PACKAGE + _angle +
                            SPLIT_PACKAGE + END_OF_PACKAGE)
        self.socket.emit("position", data={
            "code" : code,
            "angle" : _angle
        })