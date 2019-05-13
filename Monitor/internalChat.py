
from mattermostdriver import Driver
import logging
import helper
interChat = Driver({
        """
        Required options

        Instead of the login/password, you can also use a personal access token.
        If you have a token, you don't need to pass login/pass.
        """
        
        'url': 'sms.huihuang100.com',
        'login_id': 'bot@admin.com',
        'password': 'a123456',
        'token': '',

        """
        Optional options

        These options already have useful defaults or are just not needed in every case.
        In most cases, you won't need to modify these, especially the basepath.
        If you can only use a self signed/insecure certificate, you should set
        verify to False. Please double check this if you have any errors while
        using a self signed certificate!
        """
        'scheme': 'https',
        'port': 443,
        'basepath': '/api/v4',
        'verify': True,
        'mfa_token': '',


        'timeout': 30,

        """
        Setting debug to True, will activate a very verbose logging.
        This also activates the logging for the requests package,
        so you can see every request you send.

        Be careful. This SHOULD NOT be active in production, because this logs a lot!
        Even the password for your account when doing driver.login()!
        """
        'debug': False
    })
def init():
    interChat.login()    

def sendMsgToTest(msg):
    if not interChat:
        logging.error("无效的聊天室")
        return
    try:
        channel_id = interChat.channels.get_channel_by_name_and_team_name('lygj', helper.CHANEL_NAME)['id']
        interChat.posts.create_post(options={
            'channel_id': channel_id,
            'message': msg
        })
    except:
        logging.error("发送聊天失败")