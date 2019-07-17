

from PYRobot.libs.client import Client
from PYRobot.libs.client_camera import ClientCamera
import time

robot=Client("mybot")
robot.show_info()
robot.SERVICES(cam="camara_frontal/usbcam_interface")
cam=ClientCamera(robot.cam)
for x in range(1000):
    time.sleep(0.05)
    #print(type(cam.buffer))
