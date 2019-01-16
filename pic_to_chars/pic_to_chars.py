import argparse
from PIL import Image

#自定义字符画使用的字符
chars=list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
length=len(chars)
#定义命令行运行时的命令参数
parser=argparse.ArgumentParser()
parser.add_argument('-s','--src')
parser.add_argument('-o','--output')
#可以定义多个选项用于参数输入，只是-h与自带的帮助选项冲突了
parser.add_argument('-w','--width',type=int,default=40)
parser.add_argument('-hei','--height',type=int,default=40)

#解析并获取参数
args=parser.parse_args()
image=args.src
outfile=args.output
width=args.width
height=args.height

#将RGB像素值转换为对应的灰度值，不同的灰度值对应不同的字符，使用该字符代表rgb像素构成字符画
#转换公式为gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
def corresponding_char(r,g,b,alpha=256):

	if alpha==0:#表示该处为图片空白部分
		return ' '
	else:
		# 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
		gray=0.2126*r+0.7152*g+0.0722*b
		#将灰度值映射到对应的字符，相邻灰度值可能对应相同的字符
		character=chars[int(gray/((256.0+1)/length))]
		return character
if __name__ == '__main__':
	im=Image.open(image,'r')
	im=im.resize((width,height),Image.NEAREST)#转换为自定义宽高的低质量的图片
	tmp_list=''

	for i in range(height):
		for j in range(width):
			tmp_list+=corresponding_char(*im.getpixel((j,i)))#使用（j,i)是因为getpixel使用类似xy坐标的方法获取像素
		tmp_list+='\n'
	#写入文件
	if outfile:
		with open(outfile,'w') as f:
			f.write(tmp_list)
	else:
		with open('output.txt','w') as f:
			f.write(tmp_list)
