import os
from pathlib import Path
from PIL import Image
import csv
import shutil

# 将王奇的数据集添加到visDroneTXT文件内去
# img_path = '/raid/-data/00_567_all/images/train/'
img_path = '/raid/-data/00_567_all/images/val/'
# 图片文件夹
anns = os.listdir(img_path)
# anns = [ann for ann in anns if 'C00' in ann and 'C003' not in ann]
anns = [ann for ann in anns if 'C00' in ann]
# 打开文件
with open("/raid/-data/VisDrone2019/VisDrone2019-DET-val/val.txt", 'a') as outfile:
    # 图片序列
    for ann in anns:
        ans = img_path + ann + '\n'
        outfile.write(ans)
        

