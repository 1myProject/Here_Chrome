import struct
import winreg
from PIL import Image
import ctypes
import time, os,math

def rotate(down, right):
	print(down, right)
	y1=51 + 102 * (down - 1)  # вниз
	y2=37.5 + 75 * (right - 1)  # право

	x1 = 512 - y1
	x2 = 640 - y2

	print(x1,x2)

	y2=int(y2)

	u=math.atan(x1 / x2) * (180 / math.pi)
	if x2<0:
		u+=180

	u-=90
	# y1=512;y2=640

	if x1>0 and x2>0: #верхний левый
		return y1,y2,u
	elif x1>0 and x2<0: #верхний правый
		return y1,y2-256,u
	elif x1<0 and x2>0: #нижний левый
		return y1-256,y2,u
	elif x1<0 and x2<0: #нижний правый
		return y1-256,y2-256,u

def where():
	aReg=winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
	aKey=winreg.OpenKey(
		aReg,
		r"Software\Microsoft\Windows\Shell\Bags\1\Desktop",
		winreg.REG_BINARY
		)
	name, value, type_=winreg.EnumValue(aKey, 9)
	aKey.Close()
	aReg.Close()

	offset=0x10
	number_of_items=struct.unpack_from("<I", value[offset:], 8)[0]
	offset+=12
	desktop_items=[]
	for x in range(number_of_items):
		uint32_filesize=struct.unpack_from("<I", value[offset:], 4)[0];
		offset+=12
		entry_name=value[offset:(offset + (2 * uint32_filesize - 8))].decode('utf-16-le')
		offset+=(2 * uint32_filesize - 4)
		desktop_items.append([0, 0, entry_name])

	# 2nd table from behind
	offs=len(value)
	for x in range(number_of_items):
		offs-=10
		item_list=[
			struct.unpack_from("<H", value[offs:], 2)[0],  # column
			struct.unpack_from("<H", value[offs:], 6)[0],  # row
			struct.unpack_from("<H", value[offs:], 8)[0]]  # index to desktop_items
		desktop_items[item_list[-1]][0]=int(item_list[0])
		desktop_items[item_list[-1]][1]=int(item_list[1])

	for i in desktop_items:
		if i[2]==serch:
			return [i[0], i[1]]

def build(prav, vniz):
	vniz, prav, ugl=rotate(vniz, prav)

	filename='пал.png'
	palec=Image.open(filename, 'r')
	palec=palec.rotate(-ugl)

	filename1='об.jpg'
	bg=Image.open(filename1, 'r')

	itog=Image.new('RGBA', (1280, 1024), (0, 0, 0, 0))
	itog.paste(bg, (0, 0))
	itog.paste(palec, (prav, vniz), mask=palec)

	itog.save("fon.png", format="png")

	bg.close()
	palec.close()
	itog.close()

def change(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, lpath+'\\'+path, 3)

lpath=os.getcwd()
x1=[0,0]
t=1
serch='Chrome'
razmetka={
	0:1,
	16256:2,
	16384:3,
	16448:4,
	16512:5,
	16544:6,
	16576:7,
	16608:8,
	16640:9,
	16656:10,
	16672:11,
	16688:12,
	16704:13,
	16720:14,
	16736:15,
	16752:16,
	16768:17
	}
while True:
	x2= where()
	if x2==x1:
		time.sleep(t)
		continue
	else: x1=x2

	build(razmetka[x2[0]],razmetka[x2[1]])

	change('fon.png')

	time.sleep(t)
