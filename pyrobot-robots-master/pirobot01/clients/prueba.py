
from PYRobot.libs.client import Client
from PYRobot.libs.client_camera import ClientCamera
import time

robot=Client("pirobot01")
robot.show_info()

robot.SERVICES(cam="camara/picam_interface")
#robot.TOPICS("base","laser","ir","pt")
#robot.EVENTS("base_motion")
robot.connect()
cam=ClientCamera(robot.cam)
while True:
    time.sleep(0.5)
robot.close()
