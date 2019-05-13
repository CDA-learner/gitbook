#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import json
import jenkins
from jenkinsapi.api import *
import time
import sys

#
# url = 'http://172.28.128.4:9091'
# user = 'jane'
# pwd = 'A123456'
# API_Token='11bdef6880e2e81cc611b84b6b51085302'
# server = Jenkins(url, username=user, password=pwd)
# jobName = 'test-jar-shake-server'
# last_build_number = server.get_job(jobName).get_last_completed_buildnumber()
# build_info = server.get_job(jobName).get_build(last_build_number)
# print(last_build_number,build_info)
# url =build_info.get_build_url()
# print(url)
# status =build_info.get_status()
# print(status)
# print(('%s %s 部署 %s')%(jobName,url,status))

