'''
Function:
    微信小助手
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import warnings
if __name__ == '__main__':
    from modules import *
else:
    from .modules import *
warnings.filterwarnings('ignore')


'''basic info'''
BASICINFO = '''************************************************************
Function: 微信小助手 V%s
Author: Charles
微信公众号: Charles的皮卡丘
操作帮助:
    输入r: 重新初始化程序(即返回主菜单)
    输入q: 退出程序
文件默认保存路径:
    当前文件夹
************************************************************'''


'''微信小助手'''
class pikachuwechat():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_funcs = self.initializeallfuncs()
    '''非开发者运行'''
    def run(self):
        pass
    '''开发者调用对应的功能'''
    def execute(self, func_type=None, config={}):
        assert func_type in self.supported_funcs, 'unsupport func_type %s...' % func_type
        client = self.supported_funcs[func_type](**config)
        client.run()
    '''初始化所有功能'''
    def initializeallfuncs(self):
        supported_funcs = {
            'AntiWithdrawal': AntiWithdrawal,
            'AnalysisFriends': AnalysisFriends,
        }
        return supported_funcs
    '''处理用户输入'''
    def dealInput(self, tip=''):
        user_input = input(tip)
        if user_input.lower() == 'q':
            self.logger_handle.info('ByeBye...')
            sys.exit()
        elif user_input.lower() == 'r':
            self.supported_funcs = self.initializeallfuncs()
            self.run()
        else:
            return user_input


'''run'''
if __name__ == '__main__':
    wechat_helper = pikachuwechat()
    wechat_helper.execute('AnalysisFriends')