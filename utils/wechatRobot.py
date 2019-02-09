'''
Function:
	聊天机器人部分
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
from wxpy import *


'''聊天机器人'''
class wechatRobot():
	def __init__(self, **kwargs):
		self.info = 'wechatRobot'
		self.options = kwargs
	'''用于调用的函数'''
	def run(self):
		bot = Bot()
		tuling = Tuling(api_key='a65aa00b424047d88554b744eaf07597')
		@bot.register(msg_types=TEXT)
		def auto_reply_all(msg):
			tuling.do_reply(msg)
		bot.join()