#!/user/bin/env python
#
import asyncio
import json
import logging
import websockets
import threading
from server import Server
from monitorClient import MonitorClient
from optparse import OptionParser  
import os
import platform
import pyProto
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import sys
cmdCfgList = [ 'allServer' , 'serverLog', 'allGateRouteLink' ,'siteInfo', 'fix' , 'allSiteInfo' , 'exit' , 'commonServer']

html_completer = WordCompleter(cmdCfgList)

import click
logging.basicConfig(         
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='[%Y-%m_%d %H:%M:%S]',
        )

def run(monitorUrl):
    monitorClient = MonitorClient({'url' : monitorUrl})
    monitorClient.start()
    parser = OptionParser()
    parser.add_option('-s' , '--siteID' , dest = "siteID" , default = 0)
    parser.add_option('-i' , '--serverId' , dest = "serverId" , default = 0)
    parser.add_option('-t' , '--serverType' , dest = "serverType" , default = -1)
    parser.add_option('-b' , '--subType' , dest = "subType" , default = 0)
    while True:
        cmd = prompt('leying-monitor>>' , history=FileHistory('history.txt') , auto_suggest=AutoSuggestFromHistory() , completer=html_completer)
        cmdList =str.split(cmd)
        (option , args) = parser.parse_args(args = cmdList)
        siteID = int(option.siteID)
        serverType = int(option.serverType)
        subType = int(option.subType)
        serverId = int(option.serverId)
        if cmdList == []:
            continue 
        mainCmd = cmdList[0] 
        if mainCmd and mainCmd in cmdCfgList:
            if mainCmd == "exit":
                sys.exit()
                break
            monitorClient.sendGetMonitorInfoMsg()    
            if mainCmd == "allSiteInfo":
                monitorClient.cmdCallback = monitorClient.getAllSiteIDInfo
            elif mainCmd == "siteInfo":
                def callback():
                    monitorClient.getSiteInfo(siteID)
                monitorClient.cmdCallback = callback
            elif mainCmd == "commonServer":
                monitorClient.cmdCallback = monitorClient.getCommonServer
            elif mainCmd == "allServer":
                monitorClient.cmdCallback = monitorClient.getAllServer
            elif mainCmd == "allGateRouteLink":
                monitorClient.cmdCallback = monitorClient.getAllGateRouteLink
            elif mainCmd == "serverLog":
                monitorClient.cmdCallback = None
                monitorClient.sendGetLogInfoMsg(serverId,serverType,subType,siteID)
        else:
            print("无效的命令:" , mainCmd)
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-m' , '--monitorUrl' , dest = "monitorUrl" , default = "ws://172.20.100.224:9999/ws")
    (option , args) = parser.parse_args()
    monitorUrl = option.monitorUrl
    run(monitorUrl)


