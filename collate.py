import os
from pathlib import Path
from PIL import Image
import csv
import shutil

# 将指定文件夹下的txt文件路径写到txt文件里
path = ['/raid/-data/VisDrone2019/VisDrone2019-DET-test-dev',
        '/raid/-data/VisDrone2019/VisDrone2019-DET-train',
        '/raid/-data/VisDrone2019/VisDrone2019-DET-val']
dst = ['test.txt', 'train.txt', 'val.txt'] 
for i , wd in enumerate(path):
    anns = os.listdir(wd + os.sep + 'images')
    # 打开文件
    with open(wd + os.sep + dst[i], 'w') as outfile:
         # 图片序列
        for ann in anns:
            ans = wd + os.sep + 'images' + os.sep + ann + '\n'
            outfile.write(ans)

