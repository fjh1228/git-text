import os
import cv2
import argparse
from tqdm import tqdm
# import glob

img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']

def draw_bbox_oneImg_yolov5(image_path, label_path, bbox_color = (0,0,255), bbox_line = 1, bbox_fontSclae = 1):
    img = cv2.imread(image_path)
    img_height = img.shape[0]
    img_width = img.shape[1]
    if os.path.exists(label_path):
        with open(label_path) as txt_file:
            labels = txt_file.readlines()
            labels = list(filter(lambda x : x != '\n', labels))
        for data in labels:
            data_list = data.split(' ')
            if len(data_list) == 5:
                label_info = data_list[0]
                x_center = float(data_list[1])
                y_center = float(data_list[2])
                wight = float(data_list[3])
                height = float(data_list[4].strip('\n'))
                x_min = (x_center - wight/2)*img_width
                x_max = (x_center + wight/2)*img_width
                y_min = (y_center - height/2)*img_height
                y_max = (y_center + height/2)*img_height
                cv2.rectangle(img, (int(x_min),int(y_min)), (int(x_max),int(y_max)), bbox_color, bbox_line)  # 绘制bbox
                cv2.putText(img, label_info, (int(x_min),int(y_min)), cv2.FONT_HERSHEY_SIMPLEX, bbox_fontSclae, bbox_color, bbox_line, cv2.LINE_AA, False)  # 绘制标签类别
            else:
                print('labels info error with: ', label_path)  
    else:
        str_1 = 'Label file not found.'
        print(str_1, '------', image_path)
        cv2.putText(img, str_1, (0, 0), cv2.FONT_HERSHEY_SIMPLEX, bbox_fontSclae, bbox_color, bbox_line, cv2.LINE_AA, False)
    return img


def draw_bbox_yolov5(images_path, labels_path, output_path, log_message = 100, result_save = True, result_display = False, bbox_color = (0,0,255), bbox_line = 2, bbox_fontSclae = 1):
    """
        description: 在图像上绘制bbox,数据为yolov5格式
        param:
            images_path:    可以是单张图片,也可以是存有图片的文件夹
            labels_path:    图片对应的标注文件
            output_path:    绘制bbox的图片保存的文件夹路径
            result_save:    绘制结果是否保存,默认True(保存)
            result_display: 绘制结果是否展示,默认False(不展示)
            bbox_color:     bbox颜色
        return:
    """
    print('begin draw bbx\n')
    if not os.path.exists(output_path):  # 创建保存结果的文件夹
        os.makedirs(output_path,exist_ok=True)
    if os.path.isfile(images_path):  # 如果传入的是单张图片
        img_result = draw_bbox_oneImg_yolov5(images_path, labels_path, bbox_color, bbox_line, bbox_fontSclae)
        if result_display:
            cv2.imshow('result', img_result)
            cv2.waitKey(0)
        if result_save:
            result_name = os.path.basename(images_path)
            result_path = os.path.join(output_path, result_name)
            cv2.imwrite(result_path, img_result)
    else:
        # file_path_list = os.listdir(images_path)
        file_path_list = os.listdir(images_path)
        imgs_name_list = [x for x in file_path_list if x.split('.')[-1].lower() in img_formats]
        count = 0
        for img_name in tqdm(imgs_name_list):
            label_name = img_name.replace(img_name.split('.')[-1], 'txt')
            img_path = os.path.join(images_path, img_name)
            label_path = os.path.join(labels_path, label_name)
            img_result = draw_bbox_oneImg_yolov5(img_path, label_path, bbox_color, bbox_line, bbox_fontSclae)
            if result_display:
                cv2.imshow('result', img_result)
                cv2.waitKey(0)
            if result_save:
                result_path = os.path.join(output_path, img_name)
                cv2.imwrite(result_path, img_result)
            count += 1


if __name__ == '__main__':

    images_path = r"G:\00_567_all\images\train"
    labels_path = r'G:\00_567_all\labels\train'
    output_path = r'G:\00_567_all\images\test'
    draw_bbox_yolov5(images_path,labels_path,output_path)