#! usr/bin/env python
# coding:utf-8


from jenkinsapi.jenkins import Jenkins
import requests
import urllib

"""
需求1 ：感知到所有构建，并完成消息通知
需求2：群里构建后单独发消息给个人
"""
# 1. 接受jenkins返回的消息
def get_buil_msg(jobName):
    url = 'http://jenkins.ops.huihuang200.com/'
    user = 'jenkins'
    pwd = '1177e62132b6aa23f5445b878dc5d23e24'
    dict_var = {'action_name': 'deploy'}
    server = Jenkins(url, username=user, password=pwd)
    server.build_job(jobName, dict_var)
    last_build_number = server.get_job(jobName).get_last_completed_buildnumber()
    build_info = server.get_job(jobName).get_build(last_build_number)
    build_url = build_info.get_build_url() + 'console'
    build_result = build_info.get_status()
    if build_result == 'SUCCESS':
        print('build successfully \n %s \n %s')%(jobName,build_url)
    else:
        print('build Error\n %s \n %s')%(jobName,build_url)


# 2.Mattermost API 接收消息，并完成构建
def notify_1():
    url='https://sms.huihuang100.com/login'
    data ={'loginId':'869361338@qq.com','password':'123456'}
    data = urllib.parse.urlencode(data).encode('utf-8')
    connection = urllib.request.Request(url = url,data = data,method = 'GET')
    response = urllib.request.urlopen(connection)
    print(response)
    print(response.read().decode('utf-8'))

notify_1()

