#!/user/bin/env python
#
import asyncio
import json
import logging
import websockets
import threading
from server import Server
from monitorConnect import MonitorConnect
from monitorServer import MonitorServer
from optparse import OptionParser  
from logging.handlers import TimedRotatingFileHandler
import os
import platform
LOG_FILE = "/home/loguser/logs/monitor/monitor.log"
sysstr = platform.system()

logging.basicConfig(         
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='[%Y-%m_%d %H:%M:%S]',
        )

if(sysstr != "Windows"):
        fh = TimedRotatingFileHandler(LOG_FILE,when='D',interval=1,backupCount=30)
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s %(filename)s-%(lineno)d %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        

def run(port):
    monitorServer = MonitorServer()
    monitorServer.run(port)

    async def main(loop):
        logging.info("进入主循环")
        while True:
            monitorServer.update()
            await asyncio.sleep(1)    

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main(event_loop))

    logging.info("监控服务器启动")
    loop = asyncio.new_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-p' , '--port' , dest = "port" , default = 9999)
    (option , args) = parser.parse_args()
    port = int(option.port)
    run(port)


