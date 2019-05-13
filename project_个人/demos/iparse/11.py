# coding :utf -8

import re
import os
import json
import requests
import paramiko


# 开发后端API
api ='http://172.20.100.71:8080/station/getAllSiteDomains?siteId=199002'
host_name = '172.20.100.140'
username = 'deploy'
passwd ='123456'
port =22

class NGINX():

    def __init__(self, api):
        x = json.loads(requests.get(api).content)  # {"199002":["jk-888.com","www-jk888.com","jk888.app","jk888.co","jk678.com","jk888.com"]}
        server_key = list(x.keys())[0]
        server_name = str(x[server_key])[2:-2].replace("', '", " ")
        self.conf_path = '/home/nginx/conf/conf.d/'
        ssh_server = self.ssh_connect()
        self.create_conf()
        ssh_server.exec_command('')

    def ssh_connect(self):
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host_name, port, username, passwd)
        return s

    # 创建配置文件
    def create_conf(self,keys,name):
        with open(os.path.join(self.conf_path, 'template.conf'), 'r', encoding='utf-8') as f:
            temp_tex = "".join(f.readlines())
            f.close()
        confg_tex = temp_tex.replace('SERVER_NAME', name).replace('SERVER_KEY', keys)
        try:
            with open(os.path.join(self.conf_path, keys + '.conf'), 'w') as f1:
                f1.write(confg_tex)
                f1.close()
        except IOError:
            file = open(os.path.join(self.conf_path, keys + '.conf'), 'r')