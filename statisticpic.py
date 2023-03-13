from PIL import Image
import os
'''
显示图片大小的统计情况
'''

file_path = '/raid/-data/fjh_val_data/pictures/'
 
imglist = os.listdir(file_path)
sizedir = {}
for img_name in imglist:
    imgpath = file_path + os.sep + img_name
    img = Image.open(imgpath) 
    imgSize = img.size  #大小/尺寸
    w = img.width       #图片的宽
    h = img.height      #图片的高
    size = str(w) + ',' + str(h)
    if size in sizedir:
        sizedir[size] = sizedir[size] + 1
    else :
        sizedir[size] = 1

for key ,value in sizedir.items():
	print(key,value)
