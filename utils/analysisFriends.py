'''
Function:
	微信好友分析部分
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import itchat
from pyecharts import Pie, Map


'''微信好友分析'''
class analysisFriends():
	def __init__(self, **kwargs):
		self.info = 'analysisFriends'
		self.options = kwargs
		self.friends_info = None
		self.savedir = None
	'''用于调用的函数'''
	def run(self, savedir='./results'):
		if not os.path.exists(savedir):
			os.mkdir(savedir)
		self.savedir = savedir
		self.friends_info = self.getFriendsInfo()
		self.analysisArea()
		self.analysisSex()
	'''地区分析'''
	def analysisArea(self):
		title = '微信好友国内分布'
		data = {'保密': 0}
		map_ = Map(title, width=1200, height=600)
		map_.use_theme('purple-passion')
		for each in self.friends_info.get('province'):
			if not each:
				data['保密'] += 1
			else:
				if each in data:
					data[each] += 1
				else:
					data[each] = 1
		attrs = [i for i, j in data.items()]
		values = [j for i, j in data.items()]
		map_.add('', attrs, values, maptype='china', is_visualmap=True, visual_text_color='#000')
		map_.render(os.path.join(self.savedir, '%s.html' % title))
	'''性别分析'''
	def analysisSex(self):
		title = '微信好友性别比'
		data = {'男': 0, '女': 0, '保密': 0}
		pie = Pie(title, title_pos='center')
		pie.use_theme('westeros')
		for each in self.friends_info.get('sex'):
			if each == 0:
				data['保密'] += 1
			elif each == 1:
				data['男'] += 1
			elif each == 2:
				data['女'] += 1
		attrs = [i for i, j in data.items()]
		values = [j for i, j in data.items()]
		pie.add('', attrs, values, is_label_show=True, legend_orient="vertical", legend_pos="left", radius=[30, 75], rosetype="area")
		pie.render(os.path.join(self.savedir, '%s.html' % title))
	'''获得所需的微信好友信息'''
	def getFriendsInfo(self):
		try:
			itchat.auto_login(hotReload=True)
		except:
			itchat.auto_login(hotReload=True, enableCmdQR=True)
		friends = itchat.get_friends()
		friends_info = dict(
							province = self.getKeyInfo(friends, "Province"),
							city = self.getKeyInfo(friends, "City"),
							nickname = self.getKeyInfo(friends, "Nickname"),
							sex = self.getKeyInfo(friends, "Sex"),
							signature = self.getKeyInfo(friends, "Signature"),
							remarkname = self.getKeyInfo(friends, "RemarkName"),
							pyquanpin = self.getKeyInfo(friends, "PYQuanPin")
							)
		return friends_info
	'''根据key值得到对应的信息'''
	def getKeyInfo(self, friends, key):
		return list(map(lambda friend: friend.get(key), friends))