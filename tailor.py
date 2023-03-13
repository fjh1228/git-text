import shutil
import cv2 as cv
import os
from tqdm import tqdm
import math
import argparse
from draw_bbox import draw_bbox_yolov5
from draw_bbox import draw_bbox_oneImg_yolov5

'''
按照一定的要求裁剪图片
'''

def img_show(img, cor):
    x = round(cor[0])
    y = round(cor[1])
    w = round(cor[2])
    h = round(cor[3])
    img = cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
    cv.imshow('tem_img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def yolo2norm(shape, lines):
    # yolo格式转化为xtop,ytop,w,h格式
    labels = []
    h = shape[0]
    w = shape[1]
    for line in lines:
        line = line.replace('\n', '')
        line = line.split(' ')
        line = [float(x) for x in line]
        line[0] = int(line[0])
        nw = line[3] * w
        nh = line[4] * h
        xt = line[1] * w - nw / 2
        yt = line[2] * h - nh / 2
        line[1:5] = xt, yt, nw, nh
        labels.append(line)
    return labels


def norm2yolo(imgsz, labels):
    # labels 以list形式存放
    if labels is None:
        return
    if  isinstance(imgsz,int):
        h = imgsz
        w = imgsz
    else:
        h = imgsz[0]
        w = imgsz[1]
    lines = []
    for label in labels:
        wt = label[3] / w
        ht = label[4] / h
        yt = (label[2] + label[4] * 0.5) / h
        xt = (label[1] + label[3] * 0.5) / w
        x, y, iw, ih = round(xt, 16), round( yt ,16), round(wt,16), round(ht,16)
        line = str(label[0]) + ' ' + str(x) + ' ' + str(y) + ' ' + str(iw) + ' ' + str(ih) + '\n'
        lines.append(line)
    return lines


def statistic_label_img(shape, lines, imgsz, overlap):
    # 统计单张图片中标签的平均长宽和高,labels是从txt文件中读取到的lines
    w = shape[1]
    h = shape[0]
    o = overlap
    labels = yolo2norm(shape, lines)


    miuw = 0
    miuh = 0
    n = len(labels)
    for label in labels:
        miuw += label[3]
        miuh += label[4]
    miuw = round(miuw / n)
    miuh = round(miuh / n)
    stepw = max(imgsz - miuw - int(o * w), 0.5 * imgsz)
    steph = max(imgsz - miuh - int(o * h), 0.5 * imgsz)
    n_w = math.ceil(w / stepw)
    n_h = math.ceil(h / steph)
    return [n_w, n_h, stepw, steph, labels]


def parse_opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('--imgdir', type=str, default=r'D:\desktop\cleaning\images', help='图片的文件夹')
    parser.add_argument('--savedir', type=str, default=r'D:\desktop\cleaning\ans', help='保存图片和标签的文件夹')
    parser.add_argument('--imgsz', type=int, default=640, help='图片尺寸')
    parser.add_argument('--cph', type=float, default=0.1, help='裁剪阈值，标签裁剪后小于源标签的0.1将被丢弃')
    parser.add_argument('-o', '--overlap', type=float, default=0.05, help='滑动窗口重叠部分占整个宽度或高度的比例')

    args = parser.parse_args()
    return args


def main():
    args = parse_opt()
    imgdir = args.imgdir
    savedir = args.savedir
    imgsz = args.imgsz
    cph = args.cph
    overlap = args.overlap

    imgs_name = os.listdir(imgdir)
    for imgname in tqdm(imgs_name):
        try:
            img_path = imgdir + os.sep + imgname
            img = cv.imread(img_path)
            shape = img.shape[:2]  # 排列的方法是h,w
            w = shape[1]
            h = shape[0]
            if shape[0] <= imgsz and shape[1] <= imgsz:
                if not os.path.isdir(savedir + os.sep + 'images'):
                    os.makedirs(savedir + os.sep + 'images')
                if not os.path.isdir(savedir + os.sep + 'labels'):
                    os.makedirs(savedir + os.sep + 'labels')
                shutil.copy(img_path, savedir + os.sep + 'images')
                label_path = img_path.replace('images', 'labels').split('.')[0] + '.txt'
                shutil.copy(label_path, savedir + os.sep + 'labels')
                continue
            else:
                label_path = img_path.replace('images', 'labels').split('.')[0] + '.txt'
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) == 0 or lines == None:
                        continue
                    else:
                        n_w, n_h, stepw, steph, labels = statistic_label_img(shape, lines, imgsz, overlap)
                        df_w = imgsz - stepw
                        df_h = imgsz - steph
                        for j in range(n_h):
                            for i in range(n_w):
                                idx = j * n_w + i + 1
                                # 裁剪图片部分
                                if i == n_w - 1 and j == n_h - 1:
                                    # 最后一个图片
                                    left = max(w - imgsz, 0)
                                    up = max(0, h - imgsz)
                                    right = w
                                    down = h
                                elif i == n_w - 1:
                                    # 每行的最后一个图片
                                    right = w
                                    left = max(w - imgsz, 0)
                                    up = j * (imgsz - df_h)
                                    down = (j + 1) * imgsz - j * df_h
                                elif j == n_h - 1: # 每列的最后一个图片
                                    up = max(h - imgsz, 0)
                                    down = h
                                    left = i * imgsz - i * df_w
                                    right = (i + 1) * imgsz - i * df_w
                                else:
                                    left = i * (imgsz - df_w)
                                    right = (i + 1) * imgsz - i * df_w
                                    up = j * (imgsz - df_h)
                                    down = (j + 1) * imgsz - j * df_h
                                # 复制图片
                                n_left = round(left)
                                n_down = round(down)
                                n_up = round(up)
                                n_right = round(right)
                                temp_img = img[n_up:n_down, n_left:n_right, :]
                                name, suffix = imgname.split('.')
                                new_name = name + '_' + str(idx) + '.' + suffix
                                if not os.path.isdir(savedir + os.sep + 'images'):
                                    os.makedirs(savedir + os.sep + 'images')
                                if not os.path.exists(savedir + os.sep + 'images' + os.sep + new_name):
                                    cv.imwrite(savedir + os.sep + 'images' + os.sep + new_name, temp_img)



                                # 调整标签
                                new_labels = []
                                for label in labels:
                                    lx = label[1]
                                    ly = label[2]
                                    lw = label[3]
                                    lh = label[4]
                                    if left < lx and lx < right and up < ly and down > ly:
                                        # 小标签情况，标签左上角坐标在图片内部
                                        new_lw = right - lx if lx + lw > right else lw
                                        new_lh = down - ly if ly + lh > down else lh
                                        new_x = lx - left
                                        new_y = ly - up

                                    elif left < lx + lw and lx + lw < right and up < ly + lh and down > ly + lh:
                                        # 标签左上角在图片外部，但是右下角坐标在图片内部
                                        new_lw = lx + lw - left if lx < left else lw
                                        new_lh = ly + lh - up if ly < up else lh
                                        new_x = max(0, lx - left)
                                        new_y = max(ly - up, 0)
                                    elif lx > left and lx < right and ly + lh > up and ly + lh < down:
                                        # 标签只有左下角在图片内
                                        new_lw = right - lx
                                        new_lh = ly + lh - up
                                        new_x = lx - left
                                        new_y = ly - up
                                    elif ly > up and ly < down and lx + lw > left and lx + lw < right:
                                        # 标签只有右上角在图片内部
                                        new_lw = lx + lw - left
                                        new_lh = down - ly
                                        new_x = 0
                                        new_y = ly - up
                                    elif ly < up and ly + lh > down:
                                        new_lh = down - up
                                        if (lx > left and lx < right):
                                            new_lw = right - lx if lx + lw > right else lw
                                            new_x = lx - left
                                            new_y = 0
                                        elif lx + lw > left and lx + lw < right:
                                            new_lw = lw + lx - left if lx < left else lw
                                            new_x = max(0, lx - left)
                                            new_y = 0
                                        elif lx < left and lx + lw > right:
                                            new_x = 0
                                            new_y = 0
                                            new_lw = right - left
                                    elif lx < left and lx + lw > right:
                                        new_lw = right - left
                                        if ly > up and ly < down:
                                            new_lh = down - ly if ly + lh > down else lh
                                            new_x = 0
                                            new_y = ly - up
                                        elif ly + lh > up and ly + lh < down:
                                            new_lh = ly + lh - up if ly < up else lh
                                            new_x = 0
                                            new_y = max(ly - up, 0)
                                    else:
                                        continue
                                    # img_show(temp_img.clone(), [new_x, new_y, new_lw, new_lh])
                                    area = lw * lh
                                    new_area = new_lh * new_lw
                                    if new_area / area > cph:
                                        new_labels.append([label[0], new_x, new_y, new_lw, new_lh])
                                imgshape = [down - up, right - left]
                                yolo_label = norm2yolo(imgshape, new_labels)
                                txt_name = name + '_' + str(idx) + '.txt'
                                if not os.path.isdir(savedir + os.sep + 'labels'):
                                    os.makedirs(savedir + os.sep + 'labels')
                                new_txt_path = savedir + os.sep + 'labels' + os.sep + txt_name
                                with open(new_txt_path, 'w') as f:
                                    for line in yolo_label:
                                        f.write(line)
                                draw_img_path = savedir + os.sep + 'images' + os.sep + new_name
                                draw_label_path = savedir + os.sep + 'labels' + os.sep + txt_name
                                draw_out_path = savedir + os.sep + 'bbx'
                                bbximg = draw_bbox_oneImg_yolov5(draw_img_path,draw_label_path)
                                bbx_path = os.path.join(draw_out_path, new_name)
                                cv.imwrite(bbx_path, bbximg)
        except:
            print(imgname + 'has problem')




if __name__ == '__main__':
    main()