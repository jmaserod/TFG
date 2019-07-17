#!/usr/bin/env python3
# ____________developed by paco andres_10/04/2019___________________
import sys
import os
import time
from PYRobot.libs.starter import Comp_Starter
from PYRobot.libs.utils import get_PYRobots_dir,run_component
import PYRobot.libs.config_comp as conf
import PYRobot.libs.utils_BB as BB
from PYRobot.libs.botlogging.coloramadefs import P_Log
import PYRobot.libs.parser as parser
robots_dir=get_PYRobots_dir()
sys.path.append(robots_dir)

def params(cad):
    component=parser.get_COMPONENT(cad)
    if component!="":
        robot,comp =component.split("://")
        node,comp=comp.split("/")
        return robot,node,comp
    else:
        P_Log("{} not valid sintax robot://node/component or robot://component".format(cad))
        exit()


if __name__ == '__main__':
    if len(sys.argv)==2:
        P_Log("please print start/stop/kill/status")
        exit()
    if len(sys.argv)==3:
        robot=sys.argv[1]
        dir_etc=robots_dir+robot+"/etc/"
        init=conf.get_conf(dir_etc+"init.json")
        init=[robot+"://"+x for x in init]
        if sys.argv[2]=="start":
            conf.init_ttys()
            conf.init_ethernet()
        for c in init:
            run_component("component",c,run=sys.argv[2])
