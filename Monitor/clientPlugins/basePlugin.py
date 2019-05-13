
class BasePlugin:
    
    def __init__(self ,client):
        self.client = client
        self.serverInfos = None
    def onGetServerInfo(self , serverInfos):
        self.serverInfos = serverInfos

    def forceUpdate(self):
        pass

    

    