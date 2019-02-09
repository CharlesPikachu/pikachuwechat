'''
Function:
	微信小助手主函数
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Wechat helper(微信小助手), Author: Charles, WeChat Official Accounts: Charles_pikachu(微信公众号: Charles的皮卡丘), Version: V0.1.0")
	parser.add_argument('-o', dest='option', help='Choose the function you need, including <analysisFriends>, <antiWithdrawal>, <wechatRobot> and <autoReply>.\
													(选择你需要的功能, 可选项包括: 好友分析<analysisFriends>, 消息防撤回<antiWithdrawal>, 开启自动聊天机器人<wechatRobot> 和 微信消息自动回复<autoReply>)')
	parser.add_argument('-k', dest='keywords', help='Keywords for <autoReply>, use "*" to separate if keywords is more than one.(选择autoRelpy功能时的关键词, 若有多个关键词则用*分隔)')
	parser.add_argument('-c', dest='contents', help='Contents for <autoReply>, use "*" to separate if contents is more than one.(选择autoRelpy功能时的回复内容, 若有多个回复内容则用*分隔)')
	args = parser.parse_args()
	if args.option == 'analysisFriends':
		from utils.analysisFriends import analysisFriends
		print('[INFO]: analysisFriends...')
		savedir = os.path.join(os.getcwd(), 'results')
		analysisFriends().run(savedir=savedir)
		print('[INFO]: analysis friends successfully, results saved into %s...(微信好友分析成功, 结果保存在%s...)' % (savedir, savedir))
	elif args.option == 'antiWithdrawal':
		from utils.antiWithdrawal import antiWithdrawal
		print('[INFO]: antiWithdrawal...')
		antiWithdrawal().run()
	elif args.option == 'wechatRobot':
		from utils.wechatRobot import wechatRobot
		print('[INFO]: wechatRobot...')
		wechatRobot().run()
	elif args.option == 'autoReply':
		from utils.autoReply import autoReply
		print('[INFO]: autoReply...')
		keywords = args.keywords
		contents = args.contents
		if keywords:
			keywords = keywords.split('*')
		if contents:
			contents = contents.split('*')
		autoReply().run(keywords=keywords, replycontents=contents)
	else:
		print('[INFO]: argparse error...(参数解析出错, 可选项必须是<analysisFriends>, <antiWithdrawal>, <wechatRobot> 或 <autoReply>)')