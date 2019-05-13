from mmpy_bot.bot import *
import re
import requests
import json
import jenkins
from jenkinsapi.jenkins import *
from jenkinsapi.job import *
from jenkinsapi.build import Build
import time
import sys


@respond_to('(.*)',re.IGNORECASE)
def all(message,something):
    print('all 进入',something)
    values = something.split()
    command_usage = '命令参数可能不匹配，正确参数：@机器人名 deploy|stop|restart 项目名称'
    jenkins_url = 'http://jenkins.ops.huihuang200.com/search/?q='
    action_list = ['deploy','stop','restart']
    if values[0].strip() in action_list:
        # try:
                action_var = values[0]
                jobnames = values[1]
                HOSTS_API = 'https://ops.huihuang200.com/api/ansible/ProjectDetailExceptProd'
                hosts_inventory = get_data(HOSTS_API, str(jobnames))
                hosts_json = json.dumps(hosts_inventory,sort_keys=True, indent=4)
                s = json.loads(hosts_json);
                if s['server_name'].strip():
                    jobName = str(s['server_name'])
                    url = 'http://jenkins.ops.huihuang200.com/'
                    user = 'jenkins'
                    pwd = '1177e62132b6aa23f5445b878dc5d23e24'
                    jobToken = 'UU8bi6wl7kOIsW6E'
                    dict_var = {'action_name': values[0]}
                    target = str(s['target'])
                    app_logs_path = str(s['app_logs_path'])
                    server = Jenkins(url, username=user, password=pwd)
                    print('开始构建jenkins',jobName)
                    #################################
                    server.build_job(jobName,dict_var)
                    message.comment('调用 CMDB API: https://ops.huihuang200.com/')
                    message.comment('开始 '+ action_var +' ' + jobnames +', '+ jobName + '...')
                    message.comment('部署服务器地址及日志路径:'+ target + ':'+ app_logs_path)
                    time.sleep(10)

                    last_build_number = server.get_job(jobName).get_last_completed_buildnumber()
                    build_info = server.get_job(jobName).get_build(last_build_number)
                    message.comment('控制台日志输出: '+ build_info.get_build_url()+'console')
                    message.comment('ibot使用命令集: https://ops.huihuang200.com/api/ansible/ibot')
                    build_result = build_info.get_status()
                    if build_result == 'SUCCESS':
                        print('success')
                        message.comment('@all '+jobnames+'环境 '+ action_var +'成功！')
                    else:
                        message.comment('@all '+jobnames+'环境 '+ action_var +'失败！')
                else:
                    message.comment('项目名称不匹配，请查看使用方法，https://ops.huihuang200.com/api/ansible/ibot')
                # if status == '0':
                #    message.comment('构建名称有误！')
        # except:# Exception as err:
        #    message.comment('构建命令参数有误,请检查程序！')
    else:
        try:
            url = 'http://openapi.tuling123.com/openapi/api/v2'
            response = requests.get(url='http://sandbox.api.simsimi.com/request.p?', params={'key':'8a405ae5-d87d-4906-808b-a304424476d9','lc':'zh','ft':'1.0','text':str(something)})
            response.encoding='utf-8'
            resp_json = json.loads(response.text)
            string = resp_json['response']
            if str(string) == '请求次数超限制!':
                message.comment('小bot累了~先让它喘口气吧！~')
            else:
                message.comment(str(string))
        except:
            message.comment(command_usage)

'''
@listen_to('int')
def help_me(message):
    # Message is replied to the sender (prefixed with @user)
    message.comment('21H')
    # Message is sent on the channel
    # message.send('I can help everybody!')
'''
def get_data(api, project):
        url = api +'?server_name='+ project
        try:
                res = requests.get(url, timeout = 5)
        except requests.RequestException as e:
                print (e)
        else:
                return res.json()