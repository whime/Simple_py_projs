#-*- coding:utf-8 -*-
from urllib import request,parse
import cityInfo
from collections import defaultdict


"""12306抢票助手,逐步完善
	author:whime
	date:2019-03-17
	"""

#关闭https证书认证
#ssl._create_default_https_context=ssl._create_unverified_context()

def tryQuery():
	#查询并处理返回的信息,注释掉的这个方法由于返回错误界面，原因未知
	# payloads={'leftTicketDTO.train_date':'2019-04-19','leftTicketDTO.from_station':'BJP','leftTicketDTO.to_station':'SHH','purpose_codes':'ADULT'}
	# res=requests.get("https://kyfw.12306.cn/otn/leftTicket/query",params=payloads,headers=header)
	# print(res.text)
	# print(res.url)
	setoffDate=input("请输入出发日期(Y-M-D)：")
	startCity=input("请输入出发城市：")
	destination=input("请输入到达城市：")
	#城市代码和城市名的字典
	citymap=defaultdict()

	for station in cityInfo.station_names.split('@'):
		if station:
			tmp=station.split('|')
			citymap[tmp[1]]=tmp[2]
	#将城市代码信息key和value调换
	reverseCityMap=dict(zip(citymap.values(),citymap.keys()))

	globals={
		'true':0
	}	#字符串转字典需要设置true变量
	tmpurl='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='\
			+setoffDate+'&leftTicketDTO.from_station='\
			+citymap[startCity]+'&leftTicketDTO.to_station='\
			+citymap[destination]+'&purpose_codes=ADULT'
	head={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	url=request.Request(url=tmpurl,headers=head)
	req=request.urlopen(url)
	txt=req.read().decode('utf-8')
	try:
		datadict=eval(txt,globals)
	except:
		print('error page:'+req.url)
		return

	n=0;c=0
	# print('|	车次		|起点---->终点|		时间段		|	耗时		|商务座特等座|	一等座	|	二等座	|')
	print(str.format('{0:>15}{1:^20}{2:>15}{3:>15}{4:>15}{5:>15}{6:>15}','车次','起点终点','时间段','耗时','商务座特等座','一等座','二等座'))
	for info in datadict['data']['result']:
		n+=1
		splitInfo=info.split('|')
		#输出格式有待调整
		print(str.format('{0:>15}{1:^20}{2:>15}{3:>15}{4:>15}{5:>15}{6:>15}',splitInfo[3],
						 reverseCityMap[splitInfo[4]]+'->'+reverseCityMap[splitInfo[5]],splitInfo[8]+'->'+splitInfo[9],splitInfo[10],splitInfo[32],splitInfo[30],splitInfo[31]))


if __name__=='__main__':
	tryQuery()
