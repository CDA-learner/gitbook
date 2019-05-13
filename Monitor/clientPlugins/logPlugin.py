from clientPlugins.basePlugin import BasePlugin
import helper
import logging

REPORT_All_TIME = 5

class LogPlugin(BasePlugin):

    def __init__(self ,client):
        BasePlugin.__init__(self , client)
        self.tickLogTime = 0
    def update(self):
        self.tickLogTime = (self.tickLogTime+1) % REPORT_All_TIME
        if self.tickLogTime == 1:
            if self.serverInfos:
                logging.info(helper.getAllClientInfo(self.client.type , self.client.url , self.serverInfos))
    def forceUpdate(self):
        logging.info(helper.getAllClientInfo(self.client.type , self.client.url , self.serverInfos))
    