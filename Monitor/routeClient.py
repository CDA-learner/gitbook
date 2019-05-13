from client import Client
import asyncio
import helper
import config
import sys
import mysql
import msgUtils
import logging
# import internalChat
from clientPlugins.logPlugin import LogPlugin
from clientPlugins.chatPlugin import ChatPlugin

sys.path.append('./pyProto')



class MsgData:
    pass

class RouteClient(Client):
    def __init__(self , config):
        Client.__init__(self, config)
        self.bRegisted = False
        self.bSendServerInfo = False
        self.msgIndex = 0
        self.callbacks = {}
        self.plugins = []
        self.plugins.append(LogPlugin(self))
        if helper.OPEN_CHAT:
            self.plugins.append(ChatPlugin(self))
        self.firstTrigger = True
    def onMessage(self, data):
        logging.debug("收到{}服务器消息".format(self.info()))
        msg = None
        if self.type == helper.C_ROUTE:
            msg = msgUtils.unpackRouteMsg(data)
        elif self.type == helper.C_GATE:
            msg = msgUtils.unpackGateMsg(data)
        else:
            logging.error("未知的消息类型拆包")
        if(msg.sendType == 1 and self.callbacks.get(msg.seq) != None):
            callback = self.callbacks.pop(msg.seq)
            callback(msg)
        else:
            self.onMsg(msg)

    def send2Route(self, siteId, userId, sendType, targetType, subTargetType, code, data, callback=None):
        msg = msgUtils.packRouteMsg(siteId, userId, sendType, targetType, subTargetType, self.msgIndex , code, data)
        self.send(msg)
        if(sendType == 0 and callback != None):
            self.callbacks[self.msgIndex] = callback
        self.msgIndex += 1

    def send2RouteSelf(self ,code, data, callback=None):
        self.send2Route(0,0, 0, 1, 0, code, data, callback)

    def reply2Route(self ,code, data, callback=None):
        self.send2Route(0,0, 1, 1, 0, code, data, callback)
    
    def send2Gate(self ,code, data, callback=None):
        msg = msgUtils.packGateMsg(0, self.msgIndex, code, data)
        self.send(msg)
        if(callback != None):
            self.callbacks[self.msgIndex] = callback
        self.msgIndex += 1

    def onConnect(self):
        if self.type == helper.C_GATE:
            RegisterDebugA2G_R = helper.createProto(500003)
            RegisterDebugA2G_R.id = config.SERVER_ID
            RegisterDebugA2G_R.type =  5
            self.send2Gate(500003, RegisterDebugA2G_R, self.onRegister)
        elif self.type == helper.C_ROUTE:
            RegisterDebugA2R_R = helper.createProto(503003)
            RegisterDebugA2R_R.id = config.SERVER_ID
            RegisterDebugA2R_R.type =  5
            self.send2Route(0, 0, 0, 1, 0, 503003, RegisterDebugA2R_R, self.onRegister)
        logging.info("成功连接{0},开始请求注册{0}".format(self.info()))

    def onDisconnect(self):
        self.plugins = []
        self.bRegisted = False

    def sendServerList(self):
        GetServerListC2A_S = helper.createProto(504002)
        servers = mysql.getResult()
        for server in servers:
            info = GetServerListC2A_S.info.add()
            info.id = server[0]
            info.ip = server[1]
            info.port = server[2]
            info.type = server[3]
            info.subType = server[4]
        self.send2Route(0, 0, 2, 0, 0, 504002, GetServerListC2A_S)

    def onRegister(self, msg):
        logging.info("{0}注册成功".format(self.info()))
        self.bRegisted = True
    def sendServerInfo(self):
        logging.debug("发送获取{}服务器消息".format(self.info()))
        GateRouteServerConnInfoReq = helper.createProto(900001)
        if self.type == helper.C_ROUTE:
            self.send2RouteSelf(900001, GateRouteServerConnInfoReq, self.onGetServerInfo)
        else:
            self.send2Gate(900001, GateRouteServerConnInfoReq, self.onGetServerInfo)
    def onGetServerInfo(self, msg):
        for plugin in self.plugins:
            plugin.onGetServerInfo(msg.data)
        if self.firstTrigger:
            for plugin in self.plugins:
                    plugin.forceUpdate()  
            self.firstTrigger = False
        self.bSendServerInfo = False
    def update(self):
        if self.bRegisted and not self.bSendServerInfo:
            self.sendServerInfo()
            self.bSendServerInfo = True      
        for plugin in self.plugins:
            plugin.update()            

    def info(self):
        return helper.getClientSevInfo(self.type, self.url)

if __name__ == "__main__":
    c = RouteClient({'url' : 'ws://localhost:8020/ro'})
    c.start()
    asyncio.get_event_loop().run_forever()
