'''
Function:
    微信好友分析
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import itchat
from ..utils import Logger, checkDir
from pyecharts.charts import Pie, Map
from pyecharts import options as opts


'''微信好友分析'''
class AnalysisFriends():
    func_name = '微信好友分析'
    logger_handle = Logger(func_name+'.log')
    def __init__(self, **kwargs):
        self.options = kwargs
        self.savedir = kwargs.get('savedir', 'results')
        checkDir(self.savedir)
    '''外部调用运行'''
    def run(self):
        # 登录
        try: itchat.auto_login(hotReload=True)
        except: itchat.auto_login(hotReload=True, enableCmdQR=True)
        # 获得所有好友信息
        AnalysisFriends.logger_handle.info('run getFriendsInfo...')
        friends_info = self.getFriendsInfo()
        # 分析好友地域分布
        AnalysisFriends.logger_handle.info('run analysisArea...')
        self.analysisArea(friends_info=friends_info)
        # 分析好友性别分布
        AnalysisFriends.logger_handle.info('run analysisSex...')
        self.analysisSex(friends_info=friends_info)
    '''分析好友地域分布'''
    def analysisArea(self, title='分析好友地域分布', friends_info=None):
        area_infos = {'未知': 0}
        for item in friends_info.get('province'):
            if not item: area_infos['未知'] += 1
            else:
                if item in area_infos: area_infos[item] += 1
                else: area_infos[item] = 1
        map_ = Map(init_opts=dict(theme='purple-passion', page_title=title))
        map_.add(title, data_pair=tuple(zip(area_infos.keys(), area_infos.values())), maptype='china')
        map_.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
        map_.render(os.path.join(self.savedir, '%s.html' % title))
    '''分析好友性别分布'''
    def analysisSex(self, title='分析好友性别分布', friends_info=None):
        sex_infos = {'男': 0, '女': 0, '未知': 0}
        for item in friends_info.get('sex'):
            if item == 0: sex_infos['未知'] += 1
            elif item == 1: sex_infos['男'] += 1
            elif item == 2: sex_infos['女'] += 1
        pie = Pie(init_opts=dict(theme='westeros', page_title=title)).add(title, data_pair=tuple(zip(sex_infos.keys(), sex_infos.values())), rosetype='area')
        pie.set_global_opts(title_opts=opts.TitleOpts(title=title))
        pie.render(os.path.join(self.savedir, '%s.html' % title))
    '''获得所需的微信好友信息'''
    def getFriendsInfo(self):
        friends = itchat.get_friends()
        friends_info = dict(
            province=self.getKeyInfo(friends, "Province"),
            city=self.getKeyInfo(friends, "City"),
            nickname=self.getKeyInfo(friends, "Nickname"),
            sex=self.getKeyInfo(friends, "Sex"),
            signature=self.getKeyInfo(friends, "Signature"),
            remarkname=self.getKeyInfo(friends, "RemarkName"),
            pyquanpin=self.getKeyInfo(friends, "PYQuanPin")
        )
        return friends_info
    '''根据key值得到对应的信息'''
    def getKeyInfo(self, friends, key):
        return list(map(lambda friend: friend.get(key), friends))