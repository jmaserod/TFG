#!/usr/bin/env python3
# ____________developed by paco andres_10/04/2019___________________
import sys

from PYRobot.libs.starter import Comp_Starter
import PYRobot.libs.utils as utils
import PYRobot.libs.utils_BB as BB
from PYRobot.libs.botlogging.coloramadefs import P_Log

robots_dir=utils.get_PYRobots_dir()
sys.path.append(robots_dir)

if __name__ == '__main__':
    if len(sys.argv)>=2:
        if sys.argv[1]=="start":
            server=Comp_Starter("bin","node")
            if server.uri_BB!="0.0.0.0:0":
                server.Create("PYRobot")
                server.start()
        if sys.argv[1]=="stop":
            if server.uri_BB!="0.0.0.0:0":
                server.stop()
        if sys.argv[1]=="kill":
            pids=utils.findProcessIdByName("PYRobot/node")
            for p,n in pids:
                utils.kill_process(p)
                P_Log("killing {} PID:{}".format(n,p))
        if sys.argv[1]=="status":
            st=Comp_Starter("bin","node")
            if st.uri_BB!="0.0.0.0:0":
                st.status()
