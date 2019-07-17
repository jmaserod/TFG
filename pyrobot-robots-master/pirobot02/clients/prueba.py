
from PYRobot.libs.client import Client
from PYRobot.libs.client_camera import ClientCamera
import time

robot=Client("pirobot02")
robot.show_info()

robot.SERVICES(cam="camara/camera")
robot.TOPICS_list("tracker/line")
#robot.EVENTS("base_motion")
robot.connect()
cam=ClientCamera(robot.cam)
while True:
    print(robot.line)
    time.sleep(0.02)
robot.close()
