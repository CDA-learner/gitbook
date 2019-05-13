#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import argparse
import subprocess
import requests
import time
import jenkins

JENKINS_URL = 'http://jenkins.ops.huihuang200.com/'
JENKINS_USERNAME = 'jenkins'
JENKINS_PASSWORD = '1177e62132b6aa23f5445b878dc5d23e24'


class opsjenkins(object):
    def __init__(self):
        pass

    def sleep_print(self, sleep_time):
        print( 'tasks done, now sleeping for ' + str(sleep_time) + ' seconds')
        time.sleep(sleep_time)

    def jenkins(self):
        server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        return server

    def build_by_env(self, env_name, job_name, action):
        server = self.jenkins()
        jobName = job_name.strip()
        actionName = action.strip()
        dict_var = {'action_name': actionName}
        server.build_job(name=jobName, parameters=dict_var)
        print('调用 CMDB API: https://ops.huihuang200.com/')
        print('开始 ' + actionName + ' ' + jobName + '...')
        self.sleep_print(10)
        last_build_number = server.get_job_info(jobName)['lastCompletedBuild']['number']
        build_info = server.get_build_info(jobName, last_build_number)
        print('Jenkins Console:' + build_info['url'] + 'console')
        build_result = build_info['result']
        if build_result == 'SUCCESS':
            print('@all ' + env_name + '环境 ' + jobName + ' ' + actionName + '成功！')
        else:
            print('@all ' + env_name + '环境 ' + jobName + ' ' + actionName + '失败！')

    def buildjar_by_env(self, job_name, director_id, target, action):
        server = self.jenkins()
        jobName = job_name.strip()
        actionName = action.strip()
        director_id = director_id.strip()
        dict_var = {'action_name': actionName, 'append_args': director_id, 'target': target}
        server.build_job(name=jobName, parameters=dict_var)
        print('调用 CMDB API: https://ops.huihuang200.com/')
        print('Start ' + actionName + ' ' + jobName + '...')
        self.sleep_print(10)
        last_build_number = server.get_job_info(jobName)['lastCompletedBuild']['number']
        build_info = server.get_build_info(jobName, last_build_number)
        print('Jenkins Console:' + build_info['url'] + 'console')
        build_result = build_info['result']
        if build_result == 'SUCCESS':
            print('@all ' + jobName + ' ' + actionName + 'sucessfully!')
        else:
            print('@all ' + jobName + ' ' + actionName + 'error!')
