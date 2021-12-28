'''
Function:
    微信消息防撤回
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import os
import time
import itchat
from ..utils import Logger
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE


'''微信消息防撤回'''
class AntiWithdrawal():
    msg_infos = {}
    face_package = None
    func_name = '微信消息防撤回'
    logger_handle = Logger(func_name+'.log')
    def __init__(self, **kwargs):
        self.options = kwargs
    '''外部调用运行'''
    def run(self):
        try: itchat.auto_login(hotReload=True)
        except: itchat.auto_login(hotReload=True, enableCmdQR=True)
        '''保存接收到的信息'''
        @itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
        def savemsg(msg):
            msg_receive_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 获得消息发送者信息
            if 'ActualNickName' in msg:
                msg_from_nickname = msg['ActualNickName']
                msg_from_username = msg['ActualUserName']
                friends = itchat.get_friends(update=True)
                msg_from = msg_from_nickname
                for friend in friends:
                    if msg_from_username == friend['UserName']:
                        if friend['RemarkName']:
                            msg_from = friend['RemarkName']
                        else:
                            msg_from = friend['NickName']
                        break
                groups = itchat.get_chatrooms(update=True)
                group_name = ''
                for group in groups:
                    if msg['FromUserName'] == group['UserName']:
                        group_name = group['NickName']
                        group_menber_count = group['MemberCount']
                        break
                if not group_name: group_name = '未命名群聊'
                group_name = group_name + '(%s人)' % str(group_menber_count)
                msg_from = group_name + '------->' + msg_from
            else:
                try:
                    msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
                    if not msg_from: msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
                except:
                    msg_from = 'WeChat Official Accounts'
            # 获得消息时间
            msg_send_time, msg_id, msg_content, msg_link = msg['CreateTime'], msg['MsgId'], None, None
            # 文本或者好友推荐
            if msg['Type'] in ['Text', 'Friends']:
                msg_content = msg['Text']
                AntiWithdrawal.logger_handle.info(f'Msg Type: Text or Friends, \n\tMsg Content: {msg_content}')
            # 附件/视频/图片/语音
            elif msg['Type'] in ['Attachment', 'Video', 'Picture', 'Recording']:
                msg_content = msg['FileName']
                msg['Text'](str(msg_content))
                AntiWithdrawal.logger_handle.info(f'Msg Type: Attachment or Video or Picture or Recording, \n\tMsg Content: {msg_content}')
            # 位置信息
            elif msg['Type'] in ['Map']:
                x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
                if location is None: msg_content = '纬度:' + x.__str__() + ', 经度:' + y.__str__()
                else: msg_content = location
                AntiWithdrawal.logger_handle.info(f'Msg Type: Map, \n\tMsg Content: {msg_content}')
            # 分享的音乐/文章
            elif msg['Type'] in ['Sharing']:
                msg_content, msg_link = msg['Text'], msg['Url']
                AntiWithdrawal.logger_handle.info(f'Msg Type: Sharing, \n\tMsg Content: {msg_content}')
            AntiWithdrawal.face_package = msg_content
            AntiWithdrawal.msg_infos.update({
                msg_id: {
                    'msg_from': msg_from,
                    'msg_send_time': msg_send_time,
                    'msg_receive_time': msg_receive_time,
                    'msg_type': msg['Type'],
                    'msg_content': msg_content,
                    'msg_link': msg_link,
                }
            })
            AntiWithdrawal.update()
        '''监听是否有消息撤回'''
        @itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
        def monitor(msg):
            if '撤回了一条消息' in msg['Content']:
                withdraw_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
                withdraw_msg = AntiWithdrawal.msg_infos.get(withdraw_msg_id)
                AntiWithdrawal.logger_handle.info(f'{withdraw_msg} has been withdrawn')
                if len(withdraw_msg_id) < 11:
                    itchat.send_file(AntiWithdrawal.face_package, toUserName='filehelper')
                else:
                    prompt_list = [
                        withdraw_msg.get('msg_from') + '撤回了一条消息',
                        '消息类型: ' + withdraw_msg.get('msg_type'),
                        '接收时间: ' + withdraw_msg.get('msg_receive_time'),
                        '消息内容: ' + withdraw_msg.get('msg_content'),
                    ]
                    prompt = '\n'.join(prompt_list)
                    if withdraw_msg['msg_type'] in ['Sharing']: prompt += '\n链接: ' + withdraw_msg.get('msg_link')
                    itchat.send_msg(prompt, toUserName='filehelper')
                    if withdraw_msg['msg_type'] in ['Attachment', 'Video', 'Picture', 'Recording']:
                        file_ = '@fil@%s' % (withdraw_msg['msg_content'])
                        itchat.send(msg=file_, toUserName='filehelper')
                        os.remove(withdraw_msg['msg_content'])
                    AntiWithdrawal.msg_infos.pop(withdraw_msg_id)
        itchat.run()
    '''更新消息(删除5分钟之前的消息)'''
    @staticmethod
    def update():
        need_del_msgs = []
        for msg in AntiWithdrawal.msg_infos:
            msg_time_interval = int(time.time()) - AntiWithdrawal.msg_infos[msg]['msg_send_time']
            if msg_time_interval > 5 * 60: need_del_msgs.append(msg)
        for msg in need_del_msgs: AntiWithdrawal.msg_infos.pop(msg)