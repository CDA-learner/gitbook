from monitorConnect import MonitorConnect
import msgUtils
import helper
import logging

class ServerMonitorConnect(MonitorConnect):
    def __init__(self, conn ,server):
        super().__init__(conn , server)

    def onRegisterMonitor(self):
        GateRouteServerConnInfoReq = helper.createProto(900001)
        self.send(msgUtils.packMonitorMsg(900001 , GateRouteServerConnInfoReq))
        
    def onGetServerInfo(self, data):
        for serverInfo in data.serverInfo:
            connect = self.server.getConnect(serverInfo.id)
            if connect == None:
                logging.error("{} , 没有注册到监控服务器".format(helper.getMonitorConnectInfo(serverInfo)))
            else:
                logging.info(serverInfo)
    def onMsg(self, msg):
        super().onMsg(msg)
        if(msg.code == 900002):
            self.onGetServerInfo(msg.data)
