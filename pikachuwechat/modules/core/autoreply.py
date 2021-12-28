'''
Function:
    微信消息自动回复
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import itchat
from ..utils import Logger
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE


'''自动回复的规则'''
AUTO_REPLY_RULES = {'工作': '[自动回复]: 您好, 我现在有事不在, 请稍后联系我.'}


'''微信消息自动回复'''
class AutoReply():
    func_name = '微信消息自动回复'
    logger_handle = Logger(func_name+'.log')
    def __init__(self, **kwargs):
        self.options = kwargs
        if 'auto_reply_rules' in kwargs:
            global AUTO_REPLY_RULES
            AUTO_REPLY_RULES = kwargs['auto_reply_rules']
    '''外部调用运行'''
    def run(self):
        try: itchat.auto_login(hotReload=True)
        except: itchat.auto_login(hotReload=True, enableCmdQR=True)
        '''消息自动回复'''
        @itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
        def autoreplay(msg):
            global AUTO_REPLY_RULES
            if msg['Text'] in AUTO_REPLY_RULES:
                itchat.send(AUTO_REPLY_RULES[msg['Text']], msg['FromUserName'])
                AutoReply.logger_handle.info('Msg: %s,\nReplay: %s' % (msg['Text'], AUTO_REPLY_RULES[msg['Text']]))
        itchat.run()