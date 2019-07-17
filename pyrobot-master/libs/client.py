import PYRobot.libs.utils_BB as BB
from PYRobot.libs.proxy import Proxy
from PYRobot.libs.botlogging.botlogging import Logging
from PYRobot.libs.subscription_mqtt import subscriptions

broadcast_port=9999

class Client(Logging):
    def __init__(self,robot,broadcast=broadcast_port):
        self._etc={}
        self._PROC={}
        self._PROC["event_handlers"]={}
        super().__init__()
        self._etc["name"]=robot
        self.robot=robot
        self._etc["BB_uri"]=BB.Get_BigBrother(port=broadcast)
        self._etc["BB"]=Proxy(self._etc["BB_uri"])
        if self._etc["BB"]():
            self._etc["BROKER"]=self._etc["BB"].Broker(self.robot)
            self._etc["TOPICS"]=self._etc["BB"].Topics(robot)
            self._etc["SERVICES"]=self._etc["BB"].Services(robot)
            self._etc["EVENTS"]=self._etc["BB"].Events(robot)
            self._PROC["SUB"]=subscriptions(robot+"/client",self._etc["BROKER"],self)
        else:
            self.L_error("Conneting BIGBROTHER on {}".format(self._etc["BB"]))
            exit()

    def connect(self):
        self._PROC["SUB"].connect()

    def close(self):
        self._PROC["SUB"].stop()
        try:
            for I in self._etc["SERVICES"]:
                s=getattr(self,I)
                s._close()
            self._etc["BB"]._close()
        except:
            raise
            self.L_error("{} Error stoping".format(I))


    def SERVICES(self,**services):
        robot=self._etc["name"]
        self._etc["SERVICES"]={}
        available=self._etc["BB"].Services(self._etc["name"])
        for item,service in services.items():
            service="{}/{}".format(self._etc["name"],service)
            if service in available:
                uri=self._etc["BB"].Get_Interface_Uri(service)
                if uri!="0.0.0.0:0":
                    proxy=Proxy(uri)
                    if proxy():
                        setattr(self,item,proxy)
                        self.L_info("{} Connected".format(item,uri))
                    else:
                        self.L_error("Conneting {} on {}".format(item,uri))
                        exit()
                else:
                    self.L_error("{} Not Found".format(service))
                    exit()
            else:
                self.L_error("{} Not available".format(service))
                exit()


    def TOPICS_list(self,*topics):
        available=self._etc["BB"].Topics(self._etc["name"])
        TOPICS={}
        for t in topics:
            t="{}/{}".format(self._etc["name"],t)
            if t in available:
                robot,comp,topic=t.split("/")
                setattr(self,topic,None)
                TOPICS[topic]=t
            else:
                self.L_error("Topic {} Not Found".format(t))
                exit()
        self._PROC["SUB"].subscribe_topics(**TOPICS)
        self._PROC["SUB"].connect()
        self.L_info("Topics {} Subcripted".format(",".join(topics)))

    def TOPICS(self,**topics):
        available=self._etc["BB"].Topics(self._etc["name"])
        TOPICS={}
        for t,v in topics.items():
            v="{}/{}".format(self._etc["name"],v)
            if v in available:
                robot,comp,topic=v.split("/")
                setattr(self,t,None)
                TOPICS[t]=v
            else:
                self.L_error("Topic {} Not Found".format(t))
                exit()
        self._PROC["SUB"].subscribe_topics(**TOPICS)
        self._PROC["SUB"].connect()
        self.L_info("Topics {} Subcripted".format(",".join(topics)))

    def EVENTS(self,**events):
        EVENTS={}
        available=self._etc["BB"].Events(self._etc["name"])
        for e,v in events.items():
            v="{}/{}".format(self._etc["name"],v)
            if v in available:
                setattr(self,e,[])
                EVENTS[e]=v
            else:
                self.L_error("Event {} Not Found".format(v))
                exit()
        self._PROC["SUB"].subscribe_events(**EVENTS)
        for e in EVENTS:
            self._PROC["SUB"].add_handler(e,self.on_event)
        self._PROC["SUB"].connect()
        self.L_info("Events {} Subcripted".format(",".join(events.values())))

    def add_HANDLER(self,ent_event,handler):
        if ent_event.find("::")>-1:
            entity,event = ent_event.split("::")
            available=self._etc["BB"].Events(self._etc["name"])
            if entity in available:
                self._PROC["event_handlers"][ent_event]=handler
        #print(self._PROC["event_handlers"])

    def show_info(self):
        self.L_print("Showing info from [FY]{}".format(self._etc["name"]))
        self.L_print("\t [FY]Available INTERFACES:")
        for s in self._etc["SERVICES"]:
            #interface=self._etc["BB"].Get_Interface_Uri(s)
            self.L_print("\t\t {}".format(s))
        self.L_print("\t [FY]Available TOPICS:")
        for s in self._etc["TOPICS"]:
            self.L_print("\t\t {}".format(s))
        self.L_print("\t [FY]Available EVENT channels:")
        for s in self._etc["EVENTS"]:
            self.L_print("\t\t {}".format(s))
        self.L_print("\t [FY]MQTT BROKER:[FW]{}".format(self._etc["BROKER"]))
        self.L_print("")

    def on_event(self,channel,msg):
        for e in msg:
            evhan="{}::{}".format(channel,e)
            try:
                doit=self._PROC["event_handlers"][evhan]
                doit()
            except:
                pass
