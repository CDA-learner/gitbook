
from define import PROTOS
import os
import logging
import platform
from logging.handlers import TimedRotatingFileHandler
sysstr = platform.system()

ServerTypeName = [
    "网关",
    "路由",
    "游戏",
    "记录",
    "数据库",
    "监控",
    "大厅",
    "登录",
    "后台",
    "活动",
    "文件",
    "总控",
    "代理",
    "数据回写",
]

ServerResponseMan = [
    [],
    [],
    [],
    [],
    ["bill"],
    ["bill" ,"dylan"],
    [],
    ["abe"],
    ["abe" , "mark"],
    [],
    [],
    [],
    [],
]

SubGameTypeName = [
    "游戏大厅",
    "百人奔驰",
    "飞禽走兽",
    "金蟾捕鱼",
    "斗地主",
    "百人牛牛",
    "红黑大战",
    "二人斗牛",
    "百人百家乐",
    "牛牛抢庄拼十",
    "二人麻将",
    "扎金花",
    "百人摇一摇",
    "李逵捕鱼",
    "大闹天空",
    "德州扑克",
    "寻龙夺宝",
    "十三水",
    "三张牌",
    "哪吒闹海",
    "通比牛牛",
    "龙虎斗",
    "二十一点",
    "抢庄牌九",
    "二八杠",
    "三公",
    "森林舞会",
    "血战到底",
    "水浒传",
    "追鱼传说"
]

SubGameResponseMan = [
    ["abe","mark"],
    ["caescescott"],
    ["faker"],
    ["caescescott"],
    [],
    ["caescescott"],
    ["harvey"],
    ["caescescott"],
    ["kazer"],
    ["caescescott"],
    [],
    [],
    [],
    ["caescescott"],
    [],
    [],
    [],
    [],
    [],
    ["caescescott"],
    ["caescescott"],
    ["kazer"],
    [],
    ["terry"],
    ["kazer"],
    ["terry"],
    [],
    [],
    [],
    [],
]

ServerState = [
    "未定义",
    "未注册",
    "良好运行中",
]

ClientInfo = [
    "网关",
    "路由",
]

GameServerState = [
    "沒有连接网关",
    "沒有连接路由",
    "沒有从后台获取到站点信息",
    "沒有从后台获取到房间信息",
    "沒有获取到房间库存信息",
    "正在启动",
    "正常运行",
]

DataBaseState = [
    "沒有连接网关",
    "沒有连接路由",
    "沒有连接Redis",
    "沒有连接Mysql",
    "正常运行",
]

C_GATE = 0
C_ROUTE = 1

TICK_TIME = 1

OPEN_CHAT = False

CHANEL_NAME = ''
REPORT_ALL_TIME = 3600
REPORT_DISCONNECT_TIME = 600
IS_REPORT_DISCONNECTED = False
def createProto(no):
    proto = __import__('pyProto.' + PROTOS[no]['path'].replace('/', '.') + '_pb2', globals(), locals(), [PROTOS[no]['name']])
    return getattr(proto, PROTOS[no]['name'])()

def getServerNameInfo(serverType , serverSubType):
    if serverType >= 0 and serverType < len(ServerTypeName):
        serverInfo = ServerTypeName[serverType]
    else:
        serverInfo = "未知服务器类型"
    if serverType == 2 and serverSubType >= 0 and serverSubType < len(SubGameTypeName):
        serverInfo = serverInfo + "[" + SubGameTypeName[serverSubType] + "]"
    return serverInfo

def getUrl(urlData):
    url4 = urlData & 0xFF
    url3 = (urlData >> 8) & 0xFF
    url2 = (urlData >> 16) & 0xFF
    url1 = (urlData >> 24) & 0xFF
    return "{}.{}.{}.{}".format(url1 , url2 , url3 , url4)

def getServerInfo(serverInfo):
    serverName = getServerNameInfo(serverInfo.type , serverInfo.subType)
    infoFromat = "服务器ID:{} , 服务器url:{} 服务器类型:{} , 站点ID:{} 状态:{}"
    return infoFromat.format(serverInfo.id , getUrl(serverInfo.url) , serverName , serverInfo.siteId , ServerState[serverInfo.state])

def getRouteServerInfo(info):
    infoFromat = "连接服务器数:{}个,注册服务器数:{}个"
    return infoFromat.format(info.serverLinkCount , info.serverCount)
def getGateServerInfo(info):
    infoFromat = "连接人数:{}人,注册人数:{}人,连接服务器数:{}个,注册服务器数:{}个"
    return infoFromat.format(info.playerLinkCount , info.playerCount ,info.serverLinkCount , info.serverCount)    

def getClientSevInfo(clientType , url):
    return "[{}] [ip:{}]".format(ClientInfo[clientType] , url)

def getAllClientInfo(clientType , url , data):
    def typeSort(elem):
            return elem.type
    data.serverInfo.sort(key= typeSort)
    info = "===========来自监控服务器{0}服务器信息报告===========\n".format(getClientSevInfo(clientType , url))
    if clientType == C_ROUTE:
        info += getRouteServerInfo(data)
        info += '\n'
    else:
        info += getGateServerInfo(data)
        info += '\n'
    for serverInfo in data.serverInfo:
        info += '\t\t\t\t' + getServerInfo(serverInfo)
        info += '\n'
    info += "已经挂掉的服务:\n"
    gameNoConnectList = getGameNoConnectServer(data)
    for gameIndex in gameNoConnectList:
        subGameName = SubGameTypeName[gameIndex]
        info += "\t\t\t\t" + subGameName + '\n'
    if clientType == C_ROUTE:
            serverNoConnectList = getRouteNoConnectServer(data)
            for serverType in serverNoConnectList:
                info += "\t\t\t\t" + ServerTypeName[serverType] + '\n'
    return info

def getGameNoConnectServer(serverInfos):
    noConnectGameList = []
    for gameIndex in range(len(SubGameResponseMan)):
        if SubGameResponseMan[gameIndex] != []:
            bFind = False
            for serverInfo in serverInfos.serverInfo:
                if serverInfo.type == 2 and serverInfo.subType == gameIndex:
                    bFind = True
                    break
            if not bFind:
                noConnectGameList.append(gameIndex)
    return noConnectGameList

def getRouteNoConnectServer(serverInfos):
    noConnectServerList = []
    for index in range(len(ServerResponseMan)):
        if ServerResponseMan[index] != []:
            bFind = False
            for serverInfo in serverInfos.serverInfo:
                if serverInfo.type == index:
                    bFind = True
                    break
            if not bFind:
                noConnectServerList.append(index)                    
    return noConnectServerList

def getMonitorConnectInfo(serverInfo , url):
    targetUrl = ""
    if url :
        targetUrl = url
    else:
        targetUrl = serverInfo.url
    if targetUrl == "":
        return "ID:{:<}  类型:{:^12}  站点ID:{:<}, 版本:{}".format(serverInfo.id , getServerNameInfo(serverInfo.type , serverInfo.subType) , serverInfo.siteId, serverInfo.version)
    else:
        if serverInfo.port != 0:
            return "ID:{:<}  类型:{:^12}  站点ID:{:<}  地址:{}:{} , 版本:{}".format(serverInfo.id , getServerNameInfo(serverInfo.type , serverInfo.subType) , serverInfo.siteId , targetUrl , serverInfo.port , serverInfo.version)
        else:
            return "ID:{:<}  类型:{:^12}  站点ID:{:<}  地址:{} , 版本:{}".format(serverInfo.id , getServerNameInfo(serverInfo.type , serverInfo.subType) , serverInfo.siteId , targetUrl, serverInfo.version)

def genServerId():
    id = 0
    if(sysstr != "Windows"):
        idPath = '/tmp/id.dat'
    else:
        idPath = 'id.dat'
    if os.path.exists(idPath):
        with open(idPath , 'r' , encoding = 'UTF-8') as f:
            content = f.read()
            if content == '':
                content = '1'
            id = int(content)
    id = id + 1
    with open(idPath , 'w' , encoding = 'UTF-8') as f:
        f.write(str(id))
    logging.info("gen serverId:{}".format(id))
    return id

def getSiteAllServer(siteId):
    pass

def getSiteIDList(monitorServerInfo):
    siteIDList = []
    for normalServerInfo in monitorServerInfo.normalServerInfo:
        siteId = normalServerInfo.serverInfo.siteId 
        if siteId != 0 and siteId not in siteIDList:
            siteIDList.append(siteId)
    return siteIDList

def logAllSiteIDInfo(monitorServerInfo):
    if not monitorServerInfo:
        logging.info("没有站点信息")
        return     
    siteIDList = getSiteIDList(monitorServerInfo)
    siteIDInfo = ''
    for siteID in siteIDList:
        siteIDInfo += str(siteID) + ','
    logging.info("站点信息:{}".format(siteIDInfo))
    for siteID in siteIDList:
        logSiteServerInfos(monitorServerInfo , siteID)

def getSiteServerInfos(monitorServerInfo , targetSiteID):
    servers = []
    for normalServerInfo in monitorServerInfo.normalServerInfo:
        siteId = normalServerInfo.serverInfo.siteId 
        if siteId == targetSiteID:
            servers.append(normalServerInfo)
    return servers


def getSiteServerInfo(monitorServerInfo , serverInfo):
    info = ""
    targetUrl = ''
    if serverInfo.serverInfo.url == '':
        targetUrl = getServerIp(monitorServerInfo, serverInfo.serverInfo.id)
    info += '\t'
    info += getMonitorConnectInfo(serverInfo.serverInfo , targetUrl)
    if serverInfo.serverInfo.type != 13:
        info += ", 状态:{}\n".format(getServerState(serverInfo))
    else:
        info += '\n'
    return info
def getSiteServerListInfo(monitorServerInfo , siteServerInfos):
    info = ""
    for siteServerInfo in siteServerInfos:
        info += getSiteServerInfo(monitorServerInfo , siteServerInfo)
    return info   

def getSiteServerList(siteServerInfos , bRun):
    serverList = []
    for siteServerInfo in siteServerInfos:
        if (siteServerInfo.serverInfo.type != 4 and siteServerInfo.gameServerstate == 6) or (siteServerInfo.serverInfo.type == 4 and siteServerInfo.dataBaseState == 4) or siteServerInfo.serverInfo.type == 13:
            if bRun :
                serverList.append(siteServerInfo)
        else:
            if not bRun :
                serverList.append(siteServerInfo)
    return serverList

def getSiteNoConnectServer(siteServerInfos):
    noConnectServerList = []
    for gameIndex in range(len(SubGameResponseMan)):
        if SubGameResponseMan[gameIndex] != []:
            bFind = False
            for siteServer in siteServerInfos:
                serverInfo = siteServer.serverInfo
                if serverInfo.type == 2 and serverInfo.subType == gameIndex:
                    bFind = True
                    break
            if not bFind:
                noConnectServerList.append({'type' : 2 , 'subType': gameIndex})
    findDb = False
    for siteServer in siteServerInfos:
        serverInfo = siteServer.serverInfo
        if serverInfo.type == 4:
            findDb = True
    if not findDb:
        noConnectServerList.append({'type' : 4 , 'subType': 0})
    return noConnectServerList

def getSiteNoConnectServerInfo(siteServerInfos):
    info = ""
    noConnectServerList = getSiteNoConnectServer(siteServerInfos)
    for serverInfo in noConnectServerList:
        info += '\t'
        if serverInfo['type'] == 2:
            gameIndex = serverInfo['subType']
            subGameName = SubGameTypeName[gameIndex]
            info += subGameName
        else:
            serverType = serverInfo['type']
            info += ServerTypeName[serverType]        
        info += '\n'
    return info

def getServerState(serverInfo):
    if serverInfo.serverInfo.type == 4:
        return DataBaseState[serverInfo.dataBaseState]
    else:
        return GameServerState[serverInfo.gameServerstate]

def logSiteServerInfos(monitorServerInfo , siteID):
    siteIDList = getSiteIDList(monitorServerInfo)
    if siteID not in siteIDList:
        logging.info("没有找到站点:{}".format(siteID))
        return     
    siteServerInfos = getSiteServerInfos(monitorServerInfo, siteID)
    info = "站点:{} 服务器信息\n".format(siteID)
    def typeSort(elem):
            return elem.serverInfo.type * 10 + elem.serverInfo.subType
    siteServerInfos.sort(key= typeSort)
    info += "正常运转的服务:\n"
    info += getSiteServerListInfo(monitorServerInfo , getSiteServerList(siteServerInfos , True))
    info += "\n已经挂掉的服务:\n"
    info += getSiteServerListInfo(monitorServerInfo , getSiteServerList(siteServerInfos , False))
    info += "\n没有启动的服务:\n"
    info += getSiteNoConnectServerInfo(siteServerInfos)
    logging.info(info)

def getServerIp(monitorServerInfo , serverID):
    ip = ''
    for gateRouteServerInfo in monitorServerInfo.gateRouteServerInfo:
        for serverInfo in gateRouteServerInfo.connInfos.serverInfo:
            if serverInfo.id == serverID:
                ip = getUrl(serverInfo.url)
                break
    return ip

def getCommonServerList(monitorServerInfo):
    serverList = []
    for normalServerInfo in monitorServerInfo.normalServerInfo:
        if normalServerInfo.serverInfo.type != 2 and normalServerInfo.serverInfo.type != 4 and normalServerInfo.serverInfo.type != 13:
            serverList.append(normalServerInfo)
    return serverList

def getGateRouteServerInfo(gateRouteServerInfo):
    info = '\t'
    info += getMonitorConnectInfo(gateRouteServerInfo.serverInfo , '')    
    info += "  "
    if gateRouteServerInfo.serverInfo.type == C_ROUTE:
        info += getRouteServerInfo(gateRouteServerInfo.connInfos)
    else:
        info += getGateServerInfo(gateRouteServerInfo.connInfos)
    return info

def logCommonServerListInfo(monitorServerInfo):
    logging.info("当前监控连接的所有公共服务:")
    serverList = getCommonServerList(monitorServerInfo)
    info = '\n'
    for gateRouteServerInfo in monitorServerInfo.gateRouteServerInfo:
        info += getMonitorConnectInfo(gateRouteServerInfo.serverInfo , '')    
        info += "  "
        if gateRouteServerInfo.serverInfo.type == C_ROUTE:
            info += getRouteServerInfo(gateRouteServerInfo.connInfos)
        else:
            info += getGateServerInfo(gateRouteServerInfo.connInfos)
        info += '\n'
    for server in serverList:
        targetUrl = ''
        if server.serverInfo.url == '':
            targetUrl = getServerIp(monitorServerInfo, server.serverInfo.id)
        info += getMonitorConnectInfo(server.serverInfo , targetUrl)
        if server.serverInfo.type != 13:
            info += ", 状态:{}\n".format(getServerState(server))
        else:
            info += '\n'
    logging.info(info)
    
def logAllServerListInfo(monitorServerInfo):
    info = '\n'
    logging.info("所有连接监控的服务器:")
    logging.info("监控连接服务器个数:{}个, 监控注测服务器个数:{}个".format(monitorServerInfo.connectedServerNum , monitorServerInfo.registeredServerNum))
    for gateRouteServerInfo in monitorServerInfo.gateRouteServerInfo:
        info += getGateRouteServerInfo(gateRouteServerInfo)  + '\n'
        def typeSort(elem):
            return elem.serverInfo.id
        monitorServerInfo.normalServerInfo.sort(key= typeSort)            
    for normalServerInfo in monitorServerInfo.normalServerInfo:
        info += getSiteServerInfo(monitorServerInfo , normalServerInfo)
    logging.info(info)

def logAllGateRouteLink(monitorServerInfo):
    info = '\n'
    logging.info("所有路由网关连接:")
    for gateRouteServerInfo in monitorServerInfo.gateRouteServerInfo:
        info += getGateRouteServerInfo(gateRouteServerInfo)  + '\n'
        def typeSort(elem):
            return elem.type * 10000000 + elem.subType*1000000 + elem.siteId*10 
        gateRouteServerInfo.connInfos.serverInfo.sort(key= typeSort)
        for serverInfo in gateRouteServerInfo.connInfos.serverInfo:
            info += getServerInfo(serverInfo) + '\n'
        info += '===========================================\n'
    logging.info(info)

def getLogger(serverType , serverSubType , siteId):
    LOG_FILE = "/home/loguser/logs/monitor/type_{}/subType_{}/siteId_{}/error.log".format(serverType , serverSubType , siteId)
    logger = logging.getLogger('{}_{}_{}'.format(serverType , serverSubType , siteId))
    sysstr = platform.system()
    if(sysstr == "Windows"):
        LOG_FILE = LOG_FILE[1:]
        pathList = os.path.split(LOG_FILE)
        if not os.path.exists(pathList[0]):
            os.makedirs(pathList[0])
            open(LOG_FILE , 'a').close()
    if len(logger.handlers) == 0 :
        fh = TimedRotatingFileHandler(LOG_FILE,when='D',interval=1,backupCount=30 ,encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger