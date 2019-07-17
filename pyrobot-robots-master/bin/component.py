#!/usr/bin/env python3
# ____________developed by paco andres_10/04/2019___________________
import sys
import os
import time
from PYRobot.libs.starter import Comp_Starter,Get_BigBrother_proxy
from PYRobot.libs.starter import Get_General,Get_Instance
import PYRobot.libs.utils as utils
from PYRobot.libs.botlogging.coloramadefs import P_Log
import PYRobot.libs.parser as parser
from PYRobot.libs.proxy import Proxy
robots_dir=utils.get_PYRobots_dir()
sys.path.append(robots_dir)
dir_comp=robots_dir+"components/"

def params(cad):
    component=parser.get_COMPONENT(cad)
    if component!="":
        robot,comp =component.split("://")
        node,comp=comp.split("/")
        return robot,node,comp
    else:
        P_Log("{} not valid sintax robot://node/component or robot://component".format(cad))
        exit()

def get_node(host):
    uri,bb=Get_BigBrother_proxy()
    if bb():
        return bb.Get_Node(host)
    else:
        return "0.0.0.0:0"

if __name__ == '__main__':
    myhost=utils.get_host_name()
    if len(sys.argv)<=2:
        P_Log("[ERROR] USE robot://node/component (start/stop/kill/status)")
        exit()
    if len(sys.argv)>2:
        robot,node,comp = params(sys.argv[1])
        P_Log("[FY]COMPONENT:[FW]{}://{}/{}".format(robot,node,comp))
        if sys.argv[2]=="start":
            if node in [myhost,"LOCAL"]:
                st=Comp_Starter(robot,comp)
                st.Create()
                #print(st.component)
                if st.uri_BB!="0.0.0.0:0":
                    st.Get_BB_Robot()
                    st.Get_MQTT()
                    st.Get_BB_Comp("{}/{}".format(robot,comp))
                    st.start()
                else:
                    P_Log("[FR][ERROR][FY]BigBrother Not found")
            else:
                uri=get_node(node)
                if uri=="0.0.0.0:0":
                    P_Log("[FR][ERROR][FY] Node {} not is online".format(node))
                    exit()
                else:
                    P_Log("[FY] Running in node {}:{}".format(node,uri))
                    proxy=Proxy(uri)
                    print(proxy)
                    gen=Get_General(robot)
                    print(gen)
                    ins=Get_Instance(robot,comp)
                    print(ins)

        if sys.argv[2]=="stop":
            st=Comp_Starter(robot,comp)
            if st.uri_BB!="0.0.0.0:0":
                st.stop()
        if sys.argv[2]=="status":
            st=Comp_Starter(robot,comp)
            if st.uri_BB!="0.0.0.0:0":
                st.status()
        if sys.argv[2]=="kill":
            pids=utils.findProcessIdByName(robot+"/"+comp)
            for p,n in pids:
                utils.kill_process(p)
                P_Log("killing {} PID:{}".format(n,p))
