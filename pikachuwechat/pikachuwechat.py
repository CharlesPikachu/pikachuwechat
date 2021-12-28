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
    from __init__ import __version__
else:
    from .modules import *
    from .__init__ import __version__
warnings.filterwarnings('ignore')


'''basic info'''
BASICINFO = '''************************************************************
Function: 微信小助手 V%s
Author: Charles
微信公众号: Charles的皮卡丘
************************************************************''' % (__version__)


'''微信小助手'''
class pikachuwechat():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_funcs = self.initializeallfuncs()
    '''开发者调用对应的功能'''
    def execute(self, func_type=None, config={}):
        assert func_type in self.supported_funcs, 'unsupport func_type %s...' % func_type
        client = self.supported_funcs[func_type](**config)
        client.run()
    '''初始化所有功能'''
    def initializeallfuncs(self):
        supported_funcs = {
            'AutoReply': AutoReply,
            'AntiWithdrawal': AntiWithdrawal,
            'AnalysisFriends': AnalysisFriends,
        }
        return supported_funcs
    '''获得所有支持的功能信息'''
    def getallsupported(self):
        all_supports = {}
        for key, value in self.supported_funcs.items():
            all_supports[value.func_name] = key
        return all_supports
    '''repr'''
    def __repr__(self):
        return BASICINFO


'''run'''
if __name__ == '__main__':
    import random
    wechat_helper = pikachuwechat()
    all_supports = wechat_helper.getallsupported()
    wechat_helper.execute(random.choice(list(all_supports.values())))