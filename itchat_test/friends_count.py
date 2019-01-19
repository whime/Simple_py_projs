#-*- coding: utf-8 -*-
import itchat
from matplotlib import pyplot as plt

#登录，获取好友列表
itchat.login()#会弹出一个二维码以登陆网页版微信
friends=itchat.get_friends(update=True)
#记录好友性别并画图,friends第一位为自己
male=female=other=total=0
for friend in friends[1:]:
	sex=friend['Sex']
	if sex==1:
		male+=1
	elif sex==2:
		female+=1
	else:other+=1
total=len(friends[1:])
print("friends_sum:",total)
print("male_friend:",male)
print("female_friends:",female)
print("others:",other)


#设置图形大小
plt.figure(figsize=(6,6))
lal=['male','female','others']#饼图的标签
num=[male,female,other]
colors=['blue','red','yellow']
plt.pie(num,colors=colors,labels=lal,autopct='%3.2f%%')#autopct设置保留小数点位数
plt.axis('equal')#x,y轴比例一致
plt.show()


