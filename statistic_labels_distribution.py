import os
import shutil
import argparse
import cv2  as cv
from tqdm import tqdm
'''
筛选出过大的标签的图片，然后将标签和图片全部移动到指定的目录
'''

def statistic(imgdir,labdir,bigimgdir, factor):
    # 统计一个数据集标签的整体情况
    imgs = os.listdir(imgdir)
    size = [40960 * i for i in range(11)]
    num = [0 for i in range(10)]
    bigimg = []
    for img in tqdm(imgs):

        imgname = img.split('.')[0]
        imgpath = imgdir + os.sep + img
        labpath = labdir + os.sep + imgname + '.txt'
        rgbimg = cv.imread(imgpath)
        h, w = rgbimg.shape[:2]
        with open(labpath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line.replace('\n','')
                line = line.split(' ')
                line = [ float(x) for x in line]
                line[0] = int(line[0])
                lw = line[3] * w
                lh = line[4] * h
                area = lw * lh
                for i in range(10):
                    if area >= size[i] and area < size[i + 1]:
                        num[i] += 1
                        if i >= factor:
                            if img not in bigimg:
                                bigimg.append(img)
                        break
    count = 0
    if not os.path.exists(os.path.join(bigimgdir, 'images')):
        os.makedirs(os.path.join(bigimgdir, 'images'))
    if not os.path.exists(os.path.join(bigimgdir, 'labels')):
        os.makedirs(os.path.join(bigimgdir, 'labels'))
    for bg in bigimg:
        imgpath = os.path.join(bigimgdir,'images',bg)
        if not os.path.exists(imgpath):
            shutil.move(imgdir + os.sep + bg, bigimgdir + os.sep + 'images')
            count += 1
        label_name = bg.split('.')[0] + '.txt'
        label_path = os.path.join(labdir,label_name)
        if not os.path.exists(os.path.join(bigimgdir,'labels',label_name)):
            shutil.move(label_path, bigimgdir + os.sep + 'labels')
    for i in range(10):
        print(str(i + 1) + '\t' + str(num[i]))
    print(str(count) + 'pic has been processed')

def parse_opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i','--imgdir', type=str, default=r'G:\00_567_all\images\C008', help='图片文件夹')
    parser.add_argument('-l','--labeldir', type=str, default=r'G:\00_567_all\labels\C008', help='标签文件夹')
    parser.add_argument('-b', '--bigimgdir', type=str, default=r'G:\00_567_all\images\bigimg',
                        help='筛选出来保存大于factor的图片地址')
    parser.add_argument('-f','--factor', type=int, default=1, help='大于640*640十分之1的标签图片将被筛选出来')


    opt = parser.parse_args()
    return opt

def main():
    opt = parse_opt()
    imgdir = opt.imgdir
    labeldir = opt.labeldir
    factor = opt.factor
    bigimgdir = opt.bigimgdir
    statistic(imgdir, labeldir, bigimgdir,factor)

if __name__ == '__main__':
    main()




