'''
Function:
	根据关键词自动回复部分
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import random
import itchat
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE


RELAYCONTENTS = ['[自动回复]: 您好 我现在有事不在 一会再和您联系。']
KEYWORDS = []


'''根据关键词自动回复'''
class autoReply():
	def __init__(self, **kwargs):
		self.info = 'autoReply'
		self.options = kwargs
	'''用于调用的函数'''
	def run(self, keywords=None, replycontents=None):
		if keywords is not None:
			global KEYWORDS
			KEYWORDS = keywords
		if replycontents is not None:
			global RELAYCONTENTS
			RELAYCONTENTS = replycontents
		try:
			itchat.auto_login(hotReload=True)
		except:
			itchat.auto_login(hotReload=True, enableCmdQR=True)
		itchat.run()
	'''文本消息'''
	@itchat.msg_register([TEXT], isFriendChat=True)
	def replyText(msg):
		if not KEYWORDS:
			content = random.choice(RELAYCONTENTS)
			itchat.send(content, msg['FromUserName'])
		else:
			for keyword in KEYWORDS:
				if keyword in msg['Text']:
					content = random.choice(RELAYCONTENTS)
					itchat.send(content, msg['FromUserName'])
					break
	'''其他消息'''
	@itchat.msg_register([PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
	def otherReply(msg):
		if not KEYWORDS:
			content = random.choice(RELAYCONTENTS)
			itchat.send(content, msg['FromUserName'])