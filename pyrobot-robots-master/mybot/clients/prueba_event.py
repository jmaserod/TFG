
from PYRobot.libs.client import Client
import time

robot=Client("learnbot")
robot.show_info()
robot.SERVICES("base_motion","gps_drive","pantilt_motion")
robot.TOPICS("base","laser")
robot.EVENTS("base_motion")

def on_base_left():
    global robot
    print("izq")
    b=robot.base
    robot.base_motion.set_base(b[0]+10,b[1]-10)

def on_base_right():
    global robot
    print("der")
    b=robot.base
    robot.base_motion.set_base(b[0]-5,b[1]+5)

def on_base_max():
    global robot
    print("max")


robot.add_HANDLER("base_motion::Right",on_base_right)
robot.add_HANDLER("base_motion::Left",on_base_left)
robot.add_HANDLER("base_motion::Max",on_base_max)
robot.connect()

robot.base_motion.set_base(10,600)

for i in range(300):
    print(robot.base)
    #robot.base_motion.set_base(i,i+2)
    #robot.gps_drive.set_localization(i,i,i)
    time.sleep(0.4)

robot.close()
