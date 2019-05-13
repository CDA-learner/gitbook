from connect import Connect
import msgUtils
import helper

class GateConnect(Connect):
    def __init__(self, conn):
        super().__init__(conn)

    def onMessage(self, data):
        self.onMsg(msgUtils.unpackGateServerMsg(data))

    def onRegisterDebugA2G_R(self, data):
        RegisterG2A_S = helper.createProto(500002)
        self.send(msgUtils.packGateServerMsg(data.siteId, data.userId, 500002, RegisterG2A_S))

    def onMsg(self, data):
        if(data.code == 500003):
            self.onRegisterDebugA2G_R(data)


class RouteConnect(Connect):
    def __init__(self, conn):
        super().__init__(conn)

    def onMessage(self, data):
        self.onMsg(msgUtils.unpackRouteMsg(data))

    def onRegisterA2R_R(self, data):
        RegisterR2A_S = helper.createProto(503002)
        self.send(msgUtils.packRouteMsg(0, 0, 0, 4, 0, data.seq, 503002, RegisterR2A_S))

    def onMsg(self, data):
        if(data.no == 503003):
            self.onRegisterA2R_R(data)
