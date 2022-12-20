import time
from mpu6050 import mpu6050

sensor = mpu6050(0x68)
alpha = 0.2
theta = 0.6
a0 = 0
v0 = 0
while True:
    pTime = time.time()
    a = sensor.get_accel_data()["x"]
    a -= theta
    a = a * alpha + (1 - alpha) * a0
    cTime = time.time()
    v = v0 + a * ((cTime - pTime) / 1000)
    a0 = a
    v0 = v
    pTime = cTime
    print("{}cm/s".format(v * 100))