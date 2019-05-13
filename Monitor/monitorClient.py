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

class MonitorClient(Client):
    def __init__(self , config):
        Client.__init__(self, config)
        self.monitorServerInfo = None
        self.cmdCallback = None
    def onMessage(self, data):
        msg = msgUtils.unpackMonitorMsg(data)
        self.onMsg(msg)

    def onConnect(self):
        logging.info("成功连接监控服务器:{0}".format(self.url))

    def onDisconnect(self):
        logging.info("监控服务器断开:{0}".format(self.url))

    def sendGetMonitorInfoMsg(self):
        GetMonitorServerInfoReq = helper.createProto(900015)
        self.send(msgUtils.packMonitorMsg(900015 , GetMonitorServerInfoReq))

    def sendGetLogInfoMsg(self , serverId , serverType , subType , siteId):
        GetServerErrorLogReq = helper.createProto(900018)
        GetServerErrorLogReq.serverId = serverId
        GetServerErrorLogReq.serverType = serverType
        GetServerErrorLogReq.subType = subType
        GetServerErrorLogReq.siteId = siteId
        self.send(msgUtils.packMonitorMsg(900018 , GetServerErrorLogReq))

    def onMsg(self , msg):
        logging.debug("收到服务器消息:{}".format(msg.code))
        if(msg.code == 900016):
            self.onGetMonitorServerInfo(msg.data)
        elif(msg.code == 900019): 
            self.onGetServerLog(msg.data)
    def onGetMonitorServerInfo(self, data):
        logging.info("监控服务器:{} 信息获取成功 监控版本号:{}".format(self.url ,data.monitorVersion))
        self.monitorServerInfo = data
        if self.cmdCallback:
            callback = self.cmdCallback
            callback()
    def onGetServerLog(self, data):
        logging.info("监控服务器:{} 日志获取成功".format(self.url))
        for log in data.logs:
            logging.info(log)
    def getAllSiteIDInfo(self):
        helper.logAllSiteIDInfo(self.monitorServerInfo)
        
    def getSiteInfo(self , siteID):
        helper.logSiteServerInfos(self.monitorServerInfo , siteID)

    def getCommonServer(self):
        helper.logCommonServerListInfo(self.monitorServerInfo)

    def getAllServer(self):
        helper.logAllServerListInfo(self.monitorServerInfo)

    def getAllGateRouteLink(self):
        helper.logAllGateRouteLink(self.monitorServerInfo)

if __name__ == "__main__":
    c = MonitorClient({'url' : 'ws://localhost:8020/ro'})
    c.start()
    asyncio.get_event_loop().run_forever()
