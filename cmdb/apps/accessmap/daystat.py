# -*- coding:utf-8 -*-
from pyecharts import GeoLines, Style
from pyecharts.datasets.coordinates import get_coordinate
from pyecharts.datasets.coordinates import search_coordinates_by_region_and_keyword
from pyecharts import Line
import pymongo
import time
import datetime

Webmaster_value = {
    "37640":"牛牛棋牌",
    "128303":"万国棋牌",
    "131321":"辉煌棋牌",
    "129321":"欢乐棋牌",
    "129315":"多玩棋牌",
    "129323":"乐点棋牌",
    "129326":"波克棋牌",
    "129328":"王者棋牌",
    "160687":"姚记棋牌",
    "162072":"掌上棋牌",
    "129315":"多玩棋牌",
    "162925":"91棋牌",
    "170444":"棋牌188",
    "199065":"700棋牌",
    "129333":"便民棋牌",
    "185392":"永利棋牌",
    "185404":"百胜棋牌",
    "199002":"杰克棋牌"
}

myclient = pymongo.MongoClient("mongodb://172.20.100.238:27000/")
mydb = myclient["log-service"]
mycol = mydb["lyOperationLog"]

end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
sta_time = (datetime.datetime.now()+datetime.timedelta(days=-15)).strftime("%Y-%m-%d %H:%M:%S")

data_alle = []
for x in mycol.find({"operDate":{"$gte":sta_time,"$lt":end_time},"operation":{'$regex': '登录'}},{"operDate":"1","siteId":"1","ip":"1"}):
    str_date = x["operDate"]
    date_time = str_date[0:10]
    str_ip = x["ip"]
    str_site = x["siteId"]
    data_alle.append([date_time,str_ip,str_site])

data_all = []
for ids in data_alle:
    if ids not in data_all:
        data_all.append(ids)


data_sort={}
for item in data_all:
        s = "[\'"+str(item[0])+"\',\'"+str(item[2])+"\']"
        if s in data_sort.keys():
            data_sort[s] = data_sort[s] + 1
        else:
            data_sort[s] = 1

line = Line("")

site_data = []
for item in data_sort.keys():
    key_value = str(item)+","+str(data_sort[item])
    string = key_value.replace('\'', '').replace('[', '').replace(']', '').replace(' ', '')
    last_data = string.split(',')
    site = last_data[1]
    for value in Webmaster_value.keys():
        if str(site) == str(value):
            site = Webmaster_value[value]
    site_data.append(site)

site_dist = {}
for item in site_data:
        s = str(item)
        if s in site_dist.keys():
            site_dist[s] = site_dist[s] + 1
        else:
            site_dist[s] = 1

for item in site_dist.keys():
    site_name = str(item)
    attr = []
    v = []
    for a in data_sort.keys():
        key_value = str(a)+","+str(data_sort[a])
        string = key_value.replace('\'', '').replace('[', '').replace(']', '').replace(' ', '')
        last_data = string.split(',')
        site = last_data[1]
        for value in Webmaster_value.keys():
            if str(site) == str(value):
                site = Webmaster_value[value]
        if site == site_name:
            attr.append(last_data[0])
            v.append(last_data[2])
    try:
        line.add(site_name,attr,v,is_label_show=True,yaxis_formatter=" IP",is_datazoom_show=True,)
    except BaseException:
        a = 1

line.render("/opt/jumpserver/apps/templates/daystat.html")
