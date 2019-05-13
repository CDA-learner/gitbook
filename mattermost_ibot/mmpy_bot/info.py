from mmpy_bot.bot import *
import re
import requests
import json
import jenkins
import datetime, time
from jenkinsapi.jenkins import *
from jenkinsapi.job import *
from jenkinsapi.build import Build
import time
import sys



#测试构建名称对应job名字

test_name = {
    '新奔驰宝马':['benz-bmw-game-new199'],
    '红黑大战第二版':['redblackwar-server-214','redblackwar-service-214'],
    'xxl-job-admin':['teat_xxl-job-admin237','teat_xxl-job-admin238'],
    '登陆服务lobby':['test_ game-lobby67_9091'],
    '抢庄牌九':['test_grabthecard-service160_6096'],
    'account':['test_account-service156_8080','test_account-service188_8080'],
    'activity':['test_activity-service237_9502','test_activity-service238_9502'],
    'admin':['test_admin-server205_9002','test_admin-server206_9002'],
    '代理前端':['test_agent-front'],
    '代理':['test_agent156_9090','test_agent188_9090'],
    '百家乐':['test_baccarat-server136_8022','test_baccarat-service136_8021'],
    '奔驰宝马':['test_benz-bmw-server150_9012','test_benz-bmw-service150_9022'],
    '飞禽走兽':['test_bird-beast-server150_9009','test_bird-beast-service150_9011'],
    '21点':['test_blackjack-server185_8213','test_blackjack-service185_8214'],
    '麻将之血战到底':['test_bloodyBattle-server186','test_bloodyBattle-service186'],
    'config':['test_conf-server205_9004','test_conf-server206_9004'],
    '总控前端':['test_control-front'],
    '总控':['test_control156_9092','test_control188_9092'],
    '注册中心':['test_eureka-server205_9003','test_eureka-server206_9003'],
    'file':['test_file-service233_9500','test_file-service234_9500'],
    '森林舞会':['test_forest-party-server186','test_forest-party-service186'],
    '炸金花':['test_fried-golden-server163_9101','test_fried-golden-service163_9100'],
    'game-service':['test_game-service233_9501','test_game-service234_9501'],
    '金蝉捕鱼':['test_goldcarp-server214_5091','test_goldcarp-service214_8011'],
    '抢庄牛牛':['test_grab-bullfight-server_160','test_grab-bullfight-service_160'],
    '抢庄牌九':['test_grabthecard-server160_9068','test_ grabthecard-service160_6096'],
    '百人牛牛':['test_hundred-cattle-server151_9065','test_hundred-cattle-service151_9095'],
    'hystrix':['test_hystrix205','test_hystrix206'],
    '斗地主':['test_landlord-server151_8014','test_landlord-service151_8013'],
    'log-service':['test_log-service233_8085','test_log-service234_8085'],
    '哪吒闹海':['test_nezhanaohai-fish-game-server163','test_nezhanaohai-fish-game-service163'],
    'pay-service':['test_pay-service205_8068','test_pay-service206_8068'],
    '门户前端':['test_portal-front-PC','test_portal-front-pc-91'],
    '门户':['test_portal-server237_9013','test_portal-server238_9013'],
    '摇一摇':['test_shake-server136_9010','test_shake-service136_9011'],
    '十三水':['test_shisanshui-server_159','test_shisanshui-service_159'],
    'sleuth':['test_sleuth-server205_9199','test_sleuth-server206_9199'],
    '李逵劈鱼':['test_splitfish-server209_5100','test_splitfish-service209_8111'],
    '德州扑克':['test_texasholdem-server_159','test_texasholdem-service_159'],
    '三公':['test_three-face-server185_9529','test_three-face-service185_9528'],
    '红黑大战':['test_threecardbrag-service214_8066'],
    '压庄龙虎':['test_tiger-fight-server164','test_tiger-fight-service164'],
    '同比牛牛':['test_Tongbi-cattle-server183_8036','test_tongbi-cattle-service183_8037'],
    '二人牛牛':['test_two-cattle-server209_9096','test_two-cattle-service209_9066'],
    '二八杠':['test_two-eight-server183_6056','test_two-eight-service183_6086'],
    '水浒传':['test_water_margins-server200','test_water_margins-service200'],
    '追鱼传说':['test_zhuiyuchuangshuo-server164','test_zhuiyuchuangshuo-service164'],
    '新飞禽走兽':['new-bird-beast-server'],
    '新哪吒闹海':['new-nezhanaohai-fish-server'],
    '新百人牛牛':['new-hundred-cattle'],
    '新森林舞会':[''],
    '新红黑大战':['new-redblackwar-game'],
    '新二人牛牛':['new-two-cattle-game'],
    '新同比牛牛':['new-tongbi-cattle-game'],
    '新摇一摇':['new-shake-game'],
    '新李逵劈鱼':['new-piyu'],
    '新金蟾捕鱼':['new-jinchanbuyu'],
    '新抢庄牌九':['new-qzpj-game'],
    '新游戏大厅':['new-lobby'],
    '新二八杠':['new-ebgGame'],
    '新压庄龙虎':['new-longhu'],
    '新三公':['new-tsgGame'],
    '新抢庄牛牛':['new-zhuang-cattle-game'],
    '新炸金花':['new-zjh-game'],
    '新德州扑克':['new-dzPoker'],
}


#预发布构建名称对应job名字   

yufabu_name = {
    '炸金花':['fried-golden-server82_9101','fried-golden-service82_9100'],
    '游戏大厅':['game-lobby-server84_9091','game-lobby-server85_9091'],
    '抢庄牌九':['grabthecard-server84_9068','grabthecard-service84_6096'],
    '百人牛牛':['hundred-cattle-server80_9065','hundred-cattle-service80_9095'],
    '斗地主':['landlord-server82_8014','landlord-service82_8013'],
    'account':['prere_account-service68_8080','prere_account-service71_8080'],
    'activity':['prere_activity-service147_9502','prere_activity-service148_9502'],
    'admin':['prere_admin-server63_9002','prere_admin-server64_9002'],
    '代理':['prere_agent-service68_9090','prere_agent-service71_9090'],
    '百家乐':['prere_baccarat-server76_8022','prere_baccarat-service76_8021'],
    '奔驰宝马':['prere_benz-bmw-server73_9012','prere_benz-bmw-service73_9022'],
    '飞禽走兽':['prere_bird-beast-server73_9009','prere_bird-beast-service73_9011'],
    '21点':['prere_blackjack-server112_8213','prere_blackjack-service112_8214'],
    'config':['prere_conf-server63_9004','prere_conf-server64_9004'],
    '总控':['prere_control-service68_9092','prere_control-service71_9092'],
    '注册中心':['prere_eureka-server63_9003','prere_eureka-server64_9003'],
    'file':['prere_file-service147_9500','prere_file-service148_9500'],
    'game-service':['prere_game-service147_9501','prere_game-service148_9501'],
    '金蟾捕鱼':['prere_goldcarp-server76_5091','prere_goldcarp-service76_8011'],
    '抢庄牛牛':['prere_grab-bullfight-server_174','prere_grab-bullfight-server_175'],
    'hystrix':['prere_hystrix63','prere_hystrix64'],
    'log-service':['prere_log-service68_8085','prere_log-service71_8085'],
    '哪吒闹海':['prere_nezhanaohai-fish-game-server73_5291','prere_nezhanaohai-fish-game-service73_8211'],
    'pay-serveice':['prere_pay-service63_8086','prere_pay-service64_8068'],
    '门户':['prere_portal-server68_9013','prere_portal-server71_9012'],
    '十三水':['prere_shisanshui-server_175','prere_shisanshui-service_175'],
    '监控':['prere_sleuth-server63_9199','prere_sleuth-server64_9199'],
    '德州扑克':['prere_texasholdem-server_175','prere_texasholdem-service_175'],
    '三公':['prere_three-face-service_187','prere_three-face-server_187'],
    '压庄龙虎':['prere_tiger-fight-server_187','prere_tiget-fight-service_187'],
    '同比牛牛':['prere_tongbi_cattle_server76_8036','prere_tongbi_cattle_service76_8037'],
    '二人牛牛':['prere_two-cattle-server_9096','prere_two-cattle-service_9066'],
    '二八杠':['prere_two-eight-server_187','prere_two-eight-service_187'],
    'xx-job-admin':['prere_xxl-job-admin68','prere_xxl-job-admin71'],
    '摇一摇':['shake-server80_9010','shake-service80_9011'],
    '李逵劈鱼':['splitfish-server80_5191','splitfish-service80_8111'],
    '红黑大战':['threecardbrag-server82_9068','threecardbrag-service82_8066'],
    '追鱼传说':['zhuiyuchuangshuo-server','zhuiyuchuangshuo-service'],
    '总控前端':['prere_control-front140'],
    '代理前端':['prere_agent-front140']
}


#开版构建名称对应job名字   

kaiban_name = {
    'account':['account-service162_8080'],
    '炸金花':['fried-golden-server143_9101','fried-golden-service143_9100'],
    '游戏大厅':['open-edit__game-loboy141_9091'],
    '监控':['open-edit__sleuth-server141_9199'],
    'activity':['open-edit_activity-service142_9502'],
    'admin':['open-edit_admin-server141_9002'],
    '代理前端':['open-edit_agent-front'],
    '代理':['open-edit_agent189_9090'],
    '百家乐':['open-edit_baccarat-server143_8022','open-edit_baccarat-service143_8021'],
    '奔驰宝马':['open-edit_benz-bmw-server144_9012','open-edit_benz-bmw-service144_9022'],
    '飞禽走兽':['open-edit_bird-beast-server144_9009','open-edit_bird-beast-service144_9011'],
    'config':['open-edit_conf-server141_9004'],
    '总控前端':['open-edit_control-front190'],
    '总控':['open-edit_control189_9092'],
    '注册中心':['open-edit_eureka-server141_9003'],
    'file':['open-edit_file-service142_9502'],
    'game-service':['open-edit_game-service142_9502'],
    '金蟾捕鱼':['open-edit_goldcarp-server143_5091','open-edit_goldcarp-service143_8011'],
    '抢庄牛牛':['open-edit_grab-bullfight-server_172','open-edit_grab-bullfight-service_172'],
    '百人牛牛':['open-edit_hundred-cattle-server145_9065','open-edit_hundred-cattle-service145_9095'],
    '斗地主':['open-edit_landlord-server144_8014','open-edit_landlord-service144_8013'],
    'log-service':['open-edit_log-service189_8085'],
    '哪吒闹海':['open-edit_nezhanaohai-fish-game-server171','open-edit_nezhanaohai-fish-game-service171'],
    'pay-service':['open-edit_pay-service189_8068'],
    '门户前端':['open-edit_portal-front-pc'],
    '91门户前端':['open-edit_portal-front-pc_91'],
    '门户':['open-edit_portal-server189_9012'],
    '摇一摇':['open-edit_shake-service145_9011','open-edit_shake-server145_9010'],
    '十三水':['open-edit_shisanshui-server_172','open-edit_shisanshui-service_172'],
    '李逵劈鱼':['open-edit_splitfish-server145_5191','open-edit_splitfish-service145_8111'],
    '德州扑克':['open-edit_texasholdem-server_172','open-edit_texasholdem-service_172'],
    '三公':['open-edit_three-face-server170_9528','open-edit_three-face-server170_9529'],
    '红黑大战':['open-edit_threecardbrag-server146_9068','open-edit_threecardbrag-service146_8066'],
    '压庄龙虎':['open-edit_tiger-fight-server170_9053','open-edit_tiger-fight-service170_9052'],
    '同比牛牛':['open-edit_tongbi-cattle-server170_8036','open-edit_tongbi-cattle-service170_8037'],
    '二人牛牛':['open-edit_two-cattle-server142_9096','open-edit_two-cattle-service142_9066'],
    '二八杠':['open-edit_two-eight-server170_6056','open-edit_two-eight-service171_6086'],
    'hystrix':['open_edit_develop_hystrix146'],
    'xxl-job-admin':['open_edit_xxl-job-admin146']
}


@respond_to('(.*)',re.IGNORECASE)
def all(message,something):
    values = something.split()
    if values[0] == '构建':
        try:
            jobnames = values[2]
            if values[1] == '测试':
                status = '0'
                for item in test_name.keys():
                    if str(jobnames) == str(item):
                        status = '1'
                        for navl in test_name[item]:
                            jobName = str(navl)
                            url = 'http://172.20.100.126:83/jenkins/'
                            user = 'admin'
                            pwd = 'jenkins@123'
                            jobToken = 'UU8bi6wl7kOIsW6E'
                            server = Jenkins(url=url, username=user, password=pwd)
                            server.build_job(name=jobName, token=jobToken)
                            message.comment('正在构建 '+ values[1] +' '+jobName)
                            time.sleep(10)
                            while True:
                                if len(server.get_running_builds()) == 0:
                                    break
                                else:
                                    time.sleep(10)
                            my_job =server.get_job(jobName)
                            last_build_number = my_job.get_last_completed_buildnumber()
                            # build_info = server.get_build_info(jobName, last_build_number)
                            # build_result = build_info['result']
                            build_result = my_job.get_build(last_build_number).get_status()
                            if build_result == 'SUCCESS':
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建成功！')
                            else:
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建失败！') 
                if status == '0':
                    message.comment('构建名称有误！')                                 
            elif values[1] == '开版':
                status = '0'
                for item in kaiban_name.keys():
                    if str(jobnames) == str(item):
                        status = '1'
                        for navl in kaiban_name[item]:
                            jobName = str(navl)
                            url = 'http://172.20.100.239:83/jenkins/'
                            user = 'admin'
                            pwd = 'admin123'
                            jobToken = 'UU8bi6wl7kOIsW6E'
                            server = jenkins.Jenkins(url=url, username=user, password=pwd)
                            server.build_job(name=jobName, token=jobToken)
                            message.comment('正在构建 '+ values[1] +' '+jobName)
                            time.sleep(10)
                            while True:
                                if len(server.get_running_builds()) == 0:
                                    break
                                else:
                                    time.sleep(10)
                            last_build_number = server.get_job_info(jobName)['lastCompletedBuild']['number']
                            build_info = server.get_build_info(jobName, last_build_number)
                            build_result = build_info['result']
                            if build_result == 'SUCCESS':
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建成功！')
                            else:
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建失败！') 
                if status == '0':
                    message.comment('构建名称有误！')                                 
            elif values[1] == '预发布':
                status = '0'
                for item in yufabu_name.keys():
                    if str(jobnames) == str(item):
                        status = '1'
                        for navl in yufabu_name[item]:
                            jobName = str(navl)
                            url = 'http://172.20.100.115:84/jenkins/'
                            user = 'admin'
                            pwd = 'admin123'
                            jobToken = 'UU8bi6wl7kOIsW6E'
                            server = jenkins.Jenkins(url=url, username=user, password=pwd)
                            server.build_job(name=jobName, token=jobToken)
                            message.comment('正在构建 '+ values[1] +' '+jobName)
                            time.sleep(10)
                            while True:
                                if len(server.get_running_builds()) == 0:
                                    break
                                else:
                                    time.sleep(10)
                            last_build_number = server.get_job_info(jobName)['lastCompletedBuild']['number']
                            build_info = server.get_build_info(jobName, last_build_number)
                            build_result = build_info['result']
                            if build_result == 'SUCCESS':
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建成功！')
                            else:
                                message.comment('@all '+values[1]+'环境 '+jobName+' 构建失败！') 
                if status == '0':
                    message.comment('构建名称有误！') 
            else:
                message.comment('指定环境未处理或参数有误！')
        except:
            message.comment('构建命令参数有误!')    
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
            message.comment('小bot累了~先让它喘口气吧！~')

'''
@listen_to('int')
def help_me(message):
    # Message is replied to the sender (prefixed with @user)
    message.comment('21H')

    # Message is sent on the channel
    # message.send('I can help everybody!')
'''

