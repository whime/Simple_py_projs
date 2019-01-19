#-*-coding:utf-8-*-
import itchat
import os
#使用itchat和os 模块实现远程运行cmd命令，主要用于获取小型文件

helpMsg="使用方法：\n1.cmd命令：'cmd xxx'\n2.get filename(当前目录下）\n3.关闭\n4.开启"
astflag=1  #用于控制助手功能的启用与否
absolutePath='.'

@itchat.msg_register('Text')
def reponse(msg):
	message=msg['Text']
	fromUser=msg['FromUserName']
	toUser=msg['ToUserName']
	global absolutePath,astflag
	if toUser=='filehelper':
		if message[0:3]=='cmd' and astflag==1:
			message=message[4:]#提取cmd命令
			# os.chdir(absolutePath.strip("'"))
			#判断是否为切换目录
			if message[0:2]=='cd':
					os.chdir(message[3:])
					itchat.send_msg("目录切换到"+os.getcwd(),'filehelper')
			# message='cd '+absolutePath.strip("'")+' && '+message#先打开上次用户进入的路径
			# message+=" && echo '%cd%'"#每次命令都附加输出用户进入的目录
			else:
				print(message)
				f=os.popen(message,'r')
				reply_msg=f.read()
				itchat.send_msg(reply_msg,'filehelper')
				#从返回结果取出用户当前操作的路径
				# reply_msg=reply_msg.split('\n')
				# print(reply_msg)
				# print(reply_msg[-2])
				# absolutePath=reply_msg[-2]
				# print(absolutePath)

		elif message[0:3]=='get' and astflag==1:
			# absolutefile=absolutePath+'\\'+message[4:]
			file=message[4:]
			try:
				fileexist=itchat.send_file(file,'filehelper')#发送给文件助手
				if not fileexist:
					itchat.send_msg("文件不存在！",'filehelper')
			except:
				itchat.send_msg("命令执行错误！",'filehelper')
		elif message=='关闭' or message=='3':
			if astflag==1:
				itchat.send_msg('assistant shutdown success!','filehelper')
				astflag=0
			else:
				itchat.send_msg('assistant is already shutdown.','filehelper')
		elif message=='开启' or message=='4':
			if astflag==1:
				itchat.send_msg('assistant is already start','filehelper')
			else:
				astflag=1
				itchat.send_msg('assistant is started success!','filehelper')
		else:
			if astflag==1:
				itchat.send_msg('not defined command!','filehelper')

itchat.auto_login(hotReload=True)
itchat.send_msg(helpMsg,'filehelper')
itchat.run()
