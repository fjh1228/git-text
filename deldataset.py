'''
修改train.txt内文件内容，按照字符串来删除指定的内容
'''
import os  # 只需要引入这个系统控制的库
 
# 定义一个path变量，里面是存着所以需要改的txt文件的文件夹名称
path = '/raid/-data/VisDrone2019/VisDrone2019-DET-train/train.txt'
# 系统列表出所有path文件夹里面文件的名称 （此操作并不会有序遍历所有文件，因此需要下一条代码排列）

fileName = path
file = open(fileName, 'r')  # 打开文件阅读模式
lines = file.readlines()  # 返回列表形式的内容
del_list = ['GDElNB']
# 以行为单位遍历文件内容（index是行数，line是单行内容）
for index, line in enumerate(lines):
    strT = lines[index]  # 读取当前行的内容
    bool_list = [dl in strT for dl in del_list]
    if True in bool_list:
        strT = ''
        lines[index] = strT    
file.close()
# lines列表转换为字符串放在strT中
strT = "".join(lines)
# 打开文件写入模式，把更新后的lines写进txt文件中
file = open(fileName, 'w')
file.write(strT)
file.close()
