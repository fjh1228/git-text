import os
from pathlib import Path
from PIL import Image
import csv
import shutil

'''
将visdrone数据集转换为yolo格式
'''

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2] / 2) * dw
    y = (box[1] + box[3] / 2) * dh
    w = box[2] * dw
    h = box[3] * dh
    return (x, y, w, h)
            
# wd = os.getcwd()
# path = [r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-DET-train',r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-DET-val']
path = ['/raid/-data/VisDrone2019/VisDrone2019-DET-test-dev',
        '/raid/-data/VisDrone2019/VisDrone2019-DET-train',
        '/raid/-data/VisDrone2019/VisDrone2019-DET-val']
for wd in path:
# wd = r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-DET-val'
# wd = r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-VID-test-challenge'
# wd = r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-VID-test-dev'
# wd = r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-VID-train'
# wd = r'G:\01_DataSets\04_passerby\无人机\VisDrone2019\VisDrone2019-VID-val'
    anns = os.listdir(wd + os.sep + 'annotations')
    for ann in anns:
        ans = ''
        outpath = wd + '/train/' + ann
        if ann[-3:] != 'txt':
            continue
        with Image.open(wd + '/images/' + ann[:-3] + 'jpg') as Img:
            img_size = Img.size
        with open(wd + '/annotations/' + ann, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if row[4] == '0':
                    continue
                if row[5] == '1' or row[5] =='2':
                    print(row[0],row[1],row[2],row[3],row[4],row[5])
                    bb = convert(img_size, tuple(map(int, row[:4])))
                    ans = ans + '1' + ' ' + ' '.join(str(a) for a in bb) + '\n'
                    with open(outpath, 'w') as outfile:
                        outfile.write(ans)
                    shutil.copy(wd + '/images/' + ann[:-3] + 'jpg',wd + '/train/' + ann[:-3] + 'jpg')
    # anns = os.listdir(wd + os.sep + 'train')
    # for ann in anns:
    #     if ann[-3:] != 'jpg':
    #         continue
    #     shutil.copy(wd + '/train/' + ann[:-3] + 'jpg', wd + '/train1/' + ann[:-3] + 'jpg')
    #     shutil.copy(wd + '/train/' + ann[:-3] + 'txt', wd + '/train1/' + ann[:-3] + 'txt')

