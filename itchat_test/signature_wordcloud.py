import itchat
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import PIL.Image as Image
import numpy as np
import re
"""
	使用itchat和jieba中文分词对微信好友个性前面进行统计并生成词云
"""
#登陆微信获取好友个性签名并生成词云
itchat.login()
friends=itchat.get_friends(update=True)
text=""
L=[]

rep=re.compile("<.*>")
reg=re.compile(".*?[\u4E00-\u9FA5]")#匹配中文
for i in friends:
	signature=i['Signature'].replace(' ','').replace('span','').replace('class','')
	signature=rep.sub("",signature)#去除一些表情符号导致的<emoji=>之类的文体
	signature_list=re.findall(reg,signature)#得到一个汉字组成的列表，只匹配中文
	signature=''.join(signature_list)#转换为连续的字符串
	L.append(signature)

text="".join(L)

# print(text)
#使用jieba模块分词
words=jieba.lcut(text,cut_all=True)
words=" ".join(words)#将单个词语用空格分开
print(words)

mask=np.array(Image.open("images/sheep.png"))#遮罩层用于控制生成词云的形状，这里用的是一只羊sheep.png
#font_path参数用于支持中文显示，不然中文都会显示为方框
wd=WordCloud(mask=mask,font_path = "C:\Windows\Fonts\STXINGKA.TTF").generate(words)
pic=wd.to_image()
pic.show()
plt.imshow(wd)#生成结果可以在images/signature_cloud_sheep.jpg看到
plt.axis("off")
