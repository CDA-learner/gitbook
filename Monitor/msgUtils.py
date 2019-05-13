import helper
import config
class MsgData:
    pass

def unpackRouteMsg(data):
    msg = MsgData()
    msg.siteId = int.from_bytes(data[0:4], byteorder='big')
    msg.userId = int.from_bytes(data[4:8], byteorder='big')
    msg.serverId = int.from_bytes(data[8:10], byteorder='big')
    msg.sendType = data[10]
    msg.targetType = data[11]
    msg.subTargetType = data[12]
    msg.extra = data[13]
    msg.reserved = int.from_bytes(data[14:16], byteorder='big')
    msg.seq = int.from_bytes(data[16:20], byteorder='big')
    msg.no = int.from_bytes(data[20:24], byteorder='big')
    msg.len = int.from_bytes(data[24:28], byteorder='big')
    msg.data = helper.createProto(msg.no)
    msg.data.ParseFromString(data[28:])
    return msg


def packRouteMsg(siteId, userId, sendType, targetType, subTargetType, msgIndex , code, data):
    msg = bytes()
    msg += (siteId.to_bytes(4, 'big'))
    msg += (userId.to_bytes(4, 'big'))
    msg += (config.SERVER_ID.to_bytes(2, 'big'))
    msg += (sendType.to_bytes(1, 'big'))
    msg += (targetType.to_bytes(1, 'big'))
    msg += (subTargetType.to_bytes(1, 'big'))
    msg += ((0).to_bytes(1, 'big'))
    msg += ((0).to_bytes(2, 'big'))
    msg += (msgIndex).to_bytes(4, 'big')
    msg += (code.to_bytes(4, 'big'))

    dataBytes = bytes(data.SerializeToString())
    msg += (len(dataBytes).to_bytes(4, 'big'))
    msg += (dataBytes)
    return msg


def unpackGateMsg(data):
    msg = MsgData()
    msg.siteId = int.from_bytes(data[0:4], byteorder='big')
    msg.seq = int.from_bytes(data[4:8], byteorder='big')
    msg.code = int.from_bytes(data[8:12], byteorder='big')
    msg.len = int.from_bytes(data[12:16], byteorder='big')
    msg.data = helper.createProto(msg.code)
    msg.data.ParseFromString(data[16:])
    msg.sendType = 1
    return msg

def unpackGateServerMsg(data):
    msg = MsgData()
    msg.siteId = int.from_bytes(data[0:4], byteorder='big')
    msg.userId = int.from_bytes(data[4:8], byteorder='big')
    msg.broadcast = data[8]
    msg.code = int.from_bytes(data[12:16], byteorder='big')
    msg.len = int.from_bytes(data[16:20], byteorder='big')
    msg.data = helper.createProto(msg.code)
    msg.data.ParseFromString(data[20:])
    return msg

def packGateServerMsg(siteId, userId, code, data):
    msg = bytes()
    msg += (siteId.to_bytes(4, 'big'))
    msg += (userId.to_bytes(4, 'big'))
    msg += code.to_bytes(4, 'big')
    dataBytes = bytes(data.SerializeToString())
    msg += (len(dataBytes).to_bytes(4, 'big'))
    msg += (dataBytes)
    return msg


def packGateMsg(siteId, msgIndex , code, data):
    msg = bytes()
    msg += (siteId.to_bytes(4, 'big'))
    msg += (msgIndex.to_bytes(4, 'big'))
    msg += ((0).to_bytes(4, 'big'))
    msg += (code.to_bytes(4, 'big'))
    dataBytes = bytes(data.SerializeToString())
    msg += (len(dataBytes).to_bytes(4, 'big'))
    msg += (dataBytes)
    return msg


def unpackMonitorMsg(data):
    msg = MsgData()
    msg.code = int.from_bytes(data[0:4], byteorder='big')
    msg.len = int.from_bytes(data[4:8], byteorder='big')
    msg.data = helper.createProto(msg.code)
    msg.data.ParseFromString(data[8:])
    return msg

def packMonitorMsg(code , data):
    msg = bytes()
    msg += (code.to_bytes(4, 'big'))
    dataBytes = bytes(data.SerializeToString())
    msg += (len(dataBytes).to_bytes(4, 'big'))
    msg += (dataBytes)
    return msg

