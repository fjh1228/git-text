import os
from pathlib import Path
from PIL import Image
import csv
import shutil

# 将将OA的路径添加到visDroneTXT文件内去
# path = ['/raid/-data/OAdatasets']
path = ['/raid/-data/zuozhan']
# path = ['/raid/-data/00_567_all/images/train/']
for i , wd in enumerate(path):
    for t in ['stone', 'hillside']:
        # 图片文件夹
        img_path = wd + os.sep + 'images' + os.sep + t + os.sep + 'train'
        anns = os.listdir(img_path)
        # 打开文件
        with open("/raid/-data/VisDrone2019/VisDrone2019-DET-train/train.txt", 'a') as outfile:
            # 图片序列
            # for ann in anns:
            for j, ann in enumerate(anns):
                # 这里仅添加一半的数据集
                if i % 2 == 0:
                    ans = img_path+ os.sep + ann + '\n'
                    outfile.write(ans)

