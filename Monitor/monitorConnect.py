from connect import Connect
import msgUtils
import helper
import logging
from clientPlugins.logPlugin import LogPlugin
import monitorVersion
GET_CONNECT_TIME = 10
GET_ALL_SERVER_TIME = 60
class MonitorConnect(Connect):
    def __init__(self, conn ,server):
        super().__init__(conn)
        self.registed = False
        self.connectedServersInfo = []
        self.plugins = []
        self.tickTime = 0
        self.tickNotifyAllServerTime = 0
        self.server = server
        self.gameServerstate = 0
        self.dataBaseState = 0
        self.type = 0
        self.id = 0
        self.subType = 0
        self.siteId = 0
        self.url = ""
        self.port = 0
        self.version = 0
        self.logs = []
    def onMessage(self, data):
        msgData = None
        msgType = int.from_bytes(data[0:4], byteorder='big')
        try:
            msgData = msgUtils.unpackMonitorMsg(data)
        except KeyError:
            logging.warn("无法处理的消息类型:{}".format(msgType))
        else:
            try:
                self.onMsg(msgData)
            except Exception as e:
                logging.exception(e)
                logging.error("消息处理出错:{}".format(msgType))


    def dealRegister2Monitor(self, data):
        if data.id == 0:
            self.id = helper.genServerId()
        else:
            self.id = data.id
        self.type = data.type
        self.subType = data.subType
        self.siteId = data.siteId
        self.url = data.url
        self.port = data.port
        self.version = data.version
        self.server.notifyServerList(self)
        self.server.notifyNewServer(self)
        self.onRegisterMonitor()
        self.registed = True
        logging.info("成功注册服务器:\n\t{}".format(self.getTextInfo()))
        
    def setServerInfoProto(self , infoProto):
        infoProto.id = self.id
        infoProto.type = self.type
        infoProto.subType = self.subType
        infoProto.siteId = self.siteId
        infoProto.url = self.url
        infoProto.port = self.port
        infoProto.version = self.version

    def getTextInfo(self):
        return helper.getMonitorConnectInfo(self , "")

    def onMsg(self, msg):
        if self.registed:
            logging.debug("服务:{} 收到消息:{}".format(helper.getServerNameInfo(self.type , self.subType) , msg.code))
        else:
            logging.debug("收到消息:{}".format(msg.code))
        if(msg.code == 900003):
            self.dealRegister2Monitor(msg.data)
        elif(msg.code == 900002):
            self.onGetGateRouteServerInfo(msg.data)
        elif(msg.code == 900014):
            self.onGetGameServerInfo(msg.data)
        elif(msg.code == 900015):
            self.onGetMonitorServerInfo(msg.data)
        elif(msg.code == 900017):
            self.onGetErrorLog(msg.data)
        elif(msg.code == 900018): 
            self.onGetServerLog(msg.data)            

    def onRegisterMonitor(self):
        self.requestServerInfo()
        
    def requestServerInfo(self):
        if self.isGateRouteConnect():
            GateRouteServerConnInfoReq = helper.createProto(900001)
            self.send(msgUtils.packMonitorMsg(900001 , GateRouteServerConnInfoReq))
        else:
            GetGameServerInfoReq = helper.createProto(900013)
            self.send(msgUtils.packMonitorMsg(900013 , GetGameServerInfoReq))

    def onGetGateRouteServerInfo(self, data):
        self.connectedServersInfo = data

    def onGetGameServerInfo(self, data):
        self.gameServerstate = data.gameServerstate
        self.dataBaseState = data.dataBaseState

    def onGetMonitorServerInfo(self , data):
        GetMonitorServerInfoRes = helper.createProto(900016)
        GetMonitorServerInfoRes.connectedServerNum = self.server.getConnectedServerNum()
        GetMonitorServerInfoRes.registeredServerNum = self.server.getRegistedServerNum()
        GetMonitorServerInfoRes.monitorVersion = monitorVersion.version
        for connect in self.server.getAllGateRouteConnects():
            gateRouteInfo = GetMonitorServerInfoRes.gateRouteServerInfo.add()
            connect.setServerInfoProto(gateRouteInfo.serverInfo)
            gateRouteInfo.connInfos.playerLinkCount = connect.connectedServersInfo.playerLinkCount
            gateRouteInfo.connInfos.playerCount = connect.connectedServersInfo.playerCount
            gateRouteInfo.connInfos.serverLinkCount = connect.connectedServersInfo.serverLinkCount 
            gateRouteInfo.connInfos.serverCount = connect.connectedServersInfo.serverCount 
            for serverInfo in connect.connectedServersInfo.serverInfo:
                connInfo = gateRouteInfo.connInfos.serverInfo.add()
                connInfo.id = serverInfo.id
                connInfo.state = serverInfo.state
                connInfo.type = serverInfo.type
                connInfo.subType = serverInfo.subType
                connInfo.url = serverInfo.url
                connInfo.siteId = serverInfo.siteId
        for connect in self.server.getAllNormalConnects():
            normalServerInfo = GetMonitorServerInfoRes.normalServerInfo.add()
            connect.setServerInfoProto(normalServerInfo.serverInfo)
            normalServerInfo.gameServerstate = connect.gameServerstate
            normalServerInfo.dataBaseState = connect.dataBaseState
        self.send(msgUtils.packMonitorMsg(900016 , GetMonitorServerInfoRes))

    def onGetErrorLog(self , data):
        self.logs.append('siteId:{} {}'.format(self.siteId , str(data.log)))
        if len(self.logs) > 100:
            helper.getLogger(self.type , self.subType ,self.siteId).error('\n'.join(self.logs))
            self.logs = []
    def update(self):
        for plugin in self.plugins:
            plugin.update()            
        self.tickTime = (self.tickTime+1) % GET_CONNECT_TIME
        self.tickNotifyAllServerTime = (self.tickNotifyAllServerTime+1) % GET_ALL_SERVER_TIME
        if self.tickTime == 0 and self.registed:
            self.requestServerInfo()
        if self.tickNotifyAllServerTime == 0 and self.registed:
            self.server.notifyServerList(self)

    def isGateRouteConnect(self):
        return self.type == 0 or self.type == 1

    def onGetServerLog(self , data):
        print('onGetServerLog')
        GetServerErrorLogRes = helper.createProto(900019)
        connectList = []
        if(data.serverId != 0):
            coonect = self.server.getConnectByServerId(data.serverId)
            connectList.append(coonect)
        elif data.serverType == -1:
            connectList = self.server.getConnectsByServerType(data.serverType,data.subType,data.siteId)
        else:
            connectList = self.server.getConnectsByServerType(data.serverType,data.subType,data.siteId)
        for connect in connectList:
            for log in connect.logs:
                GetServerErrorLogRes.logs.append(log)
        self.send(msgUtils.packMonitorMsg(900019 , GetServerErrorLogRes))