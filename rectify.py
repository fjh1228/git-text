'''
修改visdrone数据集的标签问题，将第一个类别由1修改成0
'''
import os  # 只需要引入这个系统控制的库
 
# 定义一个path变量，里面是存着所以需要改的txt文件的文件夹名称
path = '/raid/-data/VisDrone2019/VisDrone2019-DET-val/labels/'
# 系统列表出所有path文件夹里面文件的名称 （此操作并不会有序遍历所有文件，因此需要下一条代码排列）
total_txt = os.listdir(path)
i = 0  # 设定变量i用作命名txt文件
deleteList = []  # 设定变量deleteList，随后print出来
# 遍历前面读取的已修改的有序文件
for file in total_txt:
    fileName = path + file
    verify = 0  # 定义判断变量用来决定文件是否删除
    file = open(fileName, 'r')  # 打开文件阅读模式
    lines = file.readlines()  # 返回列表形式的内容
    # 以行为单位遍历文件内容（index是行数，line是单行内容）
    for index, line in enumerate(lines):
        strT = lines[index]  # 读取当前行的内容
        if strT[0:1] == "1":  # 切片判断前两个字符
            strT = "0"+strT[1:]  # 改成2加字符第二位往后
            lines[index] = strT  # 改写lines中的内容
            verify = 1  # 验证文件有需要保存的内容
        # 这里如果没有想要保持的就直接用空代替来写入lines中
        else:
            strT = ''
            lines[index] = strT  
    file.close()
    # lines列表转换为字符串放在strT中
    strT = "".join(lines)
    # 打开文件写入模式，把更新后的lines写进txt文件中
    file = open(fileName, 'w')
    file.write(strT)
    file.close()
