#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import argparse
import subprocess
import requests
import json
from datetime import datetime
from pyfiglet import Figlet

# pyfiglet 为字符拼凑模块

class opsdingtalk(object):
    def __init__(self):
        pass

    def get_ding_data(self, ding_type, ding_data, ci_url='/'):
        data = ''
        if ding_type == 'text':
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "",
                    "text": ""
                }
            }
            return data
        elif ding_type == 'link':
            data = {
                "msgtype": "link",
                "link": {
                    "text": "部署服务器：" + str(ding_data['target']) + "\r容器类型：" + str(
                        ding_data['server_type']) + "\r部署目录:" + str(ding_data['server_deploy_path']),
                    "title": str(ding_data['server_name']) + ' 构建成功!',
                    "picUrl": "http://img.carfree.net/jenkins.png",
                    "messageUrl": ci_url + "/job/" + ding_data['server_name']
                }
            }
            return data
        else:
            return data

    def request_dingtalk_data(self, ding_api, ding_data):
        try:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            res = requests.post(ding_api, headers=headers, data=json.dumps(ding_data), timeout=5)
        except requests.RequestException as e:
            print
            e
        else:
            return res.json()
