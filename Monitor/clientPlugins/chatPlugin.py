from clientPlugins.basePlugin import BasePlugin
import helper
import logging
# import internalChat

class ChatPlugin(BasePlugin):
    
    def __init__(self ,client):
        self.client = client
        self.tickReportTime = 0
        self.tickDisconnectTime = 0
        
    def reportAll(self):
        if self.serverInfos:
            info = helper.getAllClientInfo(self.client.type , self.client.url , self.serverInfos)
            internalChat.sendMsgToTest(info)
    def reportDisconnect(self): 
        if not helper.IS_REPORT_DISCONNECTED:
            return 
        if self.serverInfos:
            gameNoConnectList = helper.getGameNoConnectServer(self.serverInfos)
            serverNoConnectList = []
            for gameIndex in gameNoConnectList:
                responseMans = helper.SubGameResponseMan[gameIndex]
                info = ''
                for responseMan in responseMans:
                    info += '@{} @all '.format(responseMan)
                info += '你的游戏:{} 与 {} 失去连接,请火速排查'.format(helper.SubGameTypeName[gameIndex] ,helper.getClientSevInfo(self.client.type , self.client.url))
                internalChat.sendMsgToTest(info)
            if self.client.type == helper.C_ROUTE:
                serverNoConnectList = helper.getRouteNoConnectServer(self.serverInfos)
                for serverType in serverNoConnectList:
                    responseMans = helper.ServerResponseMan[serverType]
                    info = ''
                    for responseMan in responseMans:
                        info += '@{} @all '.format(responseMan)
                    info += '你的服务:{} 与 {} 失去连接,请火速排查'.format(helper.ServerTypeName[serverType] , helper.getClientSevInfo(self.client.type , self.client.url))
                    internalChat.sendMsgToTest(info)
    def update(self):
        self.tickReportTime = (self.tickReportTime+1) % helper.REPORT_ALL_TIME
        self.tickDisconnectTime = (self.tickDisconnectTime+1) % helper.REPORT_DISCONNECT_TIME
        if self.tickReportTime == 0:
            self.reportAll()
        if self.tickDisconnectTime == 0:
            self.reportDisconnect()
        
    def forceUpdate(self):
        pass
    