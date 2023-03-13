import os
from pathlib import Path
from PIL import Image
import csv
import shutil

# 将指定文件夹下的txt文件移动到指定位置
wds = ["/raid/-data/VisDrone2019/VisDrone2019-DET-test-dev",
      "/raid/-data/VisDrone2019/VisDrone2019-DET-train",
      "/raid/-data/VisDrone2019/VisDrone2019-DET-val"]
for wd in wds:
    anns = os.listdir(wd + os.sep + 'train')
    for ann in anns:
        if ann[-3:] != 'txt':
            continue
        # shutil.move(wd + '/train1/' + ann[:-3] + 'jpg', wd + '/train/' + ann[:-3] + 'jpg')
        shutil.move(wd + '/train/' + ann[:-3] + 'txt', wd + '/labels/' + ann[:-3] + 'txt')
