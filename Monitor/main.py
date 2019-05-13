#!/user/bin/env python
#

import asyncio
import json
import logging
import websockets
import threading
from routeClient import RouteClient
from ClientMgr import ClientMgr
import mysql
from server import Server
import internalChat
import helper
from optparse import OptionParser  
import jsonFileUtils
logging.basicConfig(         
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='[%Y-%m_%d %H:%M:%S]',
        )

logging.info("获取服务器列表信息")
logging.info(mysql.getResult())

envn = 'dev'

#Server.run(8011)
internalChat.init()

def run():
    datas = jsonFileUtils.getJsonDataFromFile("clientConfig.json")
    if datas == None:
        logging.error("clientConfig.json 加载失败, 监控服务器启动失败")
        return 
    
    if envn not in datas.keys():
        logging.error("clientConfig.json 加载环境{}失败, 监控服务器启动失败" , envn)
        return 
    helper.CHANEL_NAME = datas[envn]["chatChannel"]
    helper.REPORT_ALL_TIME = datas[envn]["reportAllTime"]
    helper.REPORT_DISCONNECT_TIME = datas[envn]["reportDisconnectTime"]
    helper.IS_REPORT_DISCONNECTED = datas[envn]["isReportDisconnected"]
    clientList = datas[envn]["clientList"]
    clientMgr = ClientMgr()
    clientMgr.init(clientList)
    async def main(loop):
        logging.info("进入主循环")
        while True:
            clientMgr.update()
            await asyncio.sleep(helper.TICK_TIME)

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main(event_loop))
    logging.info("监控服务器已终止")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-c' , '--chatOpen' , dest = "chat" , default = False)
    parser.add_option('-e' , '--envr' , dest = "envr" , default = 'dev')
    (option , args) = parser.parse_args()
    helper.OPEN_CHAT = bool(option.chat)
    envn = option.envr
    run()
    
    


