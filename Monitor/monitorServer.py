import logging
from server import Server
from monitorConnect import MonitorConnect
import helper
import msgUtils

class MonitorServer(Server):
    def __init__(self):
        super().__init__()

    def notifyServerList(self , conn):
        RegiterServerNotify = helper.createProto(900004)
        for connect in self.connects.values():
            if connect.registed:
                infoProto = RegiterServerNotify.serverInfo.add()
                connect.setServerInfoProto(infoProto)
        RegiterServerNotify.id = conn.id
        conn.send(msgUtils.packMonitorMsg(900004, RegiterServerNotify))

    def notifyNewServer(self, conn):
        for connect in self.connects.values():
            if connect != conn :
                RegisterServerReq = helper.createProto(900003)
                conn.setServerInfoProto(RegisterServerReq)
                connect.send(msgUtils.packMonitorMsg(900003, RegisterServerReq))

    def getConnect(self , id):
        for connect in self.connects.values():
            if connect.id == id:
                return connect 
        return None

    def getConnCls(self):
        return MonitorConnect

    def getAllGateRouteConnects(self):
        connects = []
        for connect in self.connects.values():
            if connect.isGateRouteConnect() and connect.registed:
                connects.append(connect)
        return connects

    def getAllNormalConnects(self):
        connects = []
        for connect in self.connects.values():
            if not connect.isGateRouteConnect() and connect.registed:
                connects.append(connect)
        return connects

    def getConnectedServerNum(self):
        num = 0
        for connect in self.connects.values():
            num = num + 1
        return num

    def getRegistedServerNum(self):
        num = 0
        for connect in self.connects.values():
            if connect.registed:
                num = num + 1
        return num 

    def getConnectByServerId(self , sreverId):
        for connect in self.connects.values():
            if connect.id == sreverId:
                return  connect

    def getConnectsByServerType(self , serverType , subType , siteId):
        connectList = []
        for connect in self.connects.values():
            if connect.type == serverType and connect.subType == subType:
                if siteId == 0:
                    connectList.append(connect)
                else:
                    if siteId == connect.siteId:
                        connectList.append(connect)
        return  connectList