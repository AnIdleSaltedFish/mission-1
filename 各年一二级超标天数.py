import numpy as np
import numpy as nan
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar

# 每年一级超标天数
total1 = []
# 每年二级超标天数
total2 = []
year = 2013
# 遍历根目录下的所有文件夹和文件
for root, dirs, files in os.walk('C:/Users/28166/Desktop/huanke peixun/编程任务一/Beijing'):
    # 遍历二级文件夹
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        # 一年12*365/366的所有数据
        totaldata = []
        day1 = 0
        day2 = 0
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            sum = 366
        else:
            sum = 365
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            # 处理文件
            with open(file_path, 'r') as f:
                f.readline()  # 跳过第一行
                for line in f:
                    # 获取时间字符串
                    time_str = line.split()[0]
                    # 将时间字符串转换为datetime对象
                    time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d')
                    # 使用strip()方法去除行末的换行符,然后使用split()方法将时间和数据分开,并取第一列数据
                    data = line.strip().split()[1]
                    data = float(data)
                    # 判断时间是否符合要求
                    if data == -999.000:
                        data = np.nan
                    totaldata.append(data)
        # 定义新列表
        new_list = []
        # 循环遍历长列表
        for i in range(0, len(totaldata), sum):
            # 取出每间隔12个数据的子列表
            sub_list = totaldata[i:i + sum]  # sub_list是每相邻12个数捆在一起的子列表
            new_list.append(sub_list)  # 把子列表append进去之后，new_list的元素仍是以列表的形式存在的，意思就是new_list是个二维列表
        year = year +1
        last_list = [np.nanmean(x) for x in zip(*new_list)]  # 二维列表按列求和
        print(last_list)
        print(len(last_list))
        # 在跑这一年数据的数据的时候把本年度的一级超标天和二级超标天统计出来
        for i in last_list:
            if i > 35 :
                day1 = day1 + 1
            if i > 75:
                day2 = day2 + 1
        print(day1)
        print(day2)
        total1.append(day1)
        total2.append(day2)
print(total1)
print(total2)

# 绘制折线图
x = [2013,2014,2015,2016,2017,2018,2019,2020,2021]
fig, ax = plt.subplots()
ax.plot(x, total1, 'o-', label = 'first(>35)')
ax.plot(x, total2, 'o-', label = 'second(>75)')

# 设置横轴坐标刻度

plt.title('Trend of days exceeding the standard', fontdict={'family': 'Times New Roman', 'size': 20, })
# 设置横纵坐标的名称以及对应字体格式
font2 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 14, }
plt.xlabel('Year', font2)
plt.ylabel('Number of days', font2)
# 横纵轴刻度一起设置
labels = ax.get_xticklabels() + ax.get_yticklabels()
# 设置横轴刻度旋转程度为30度
[label.set_rotation(75) for label in ax.get_xticklabels()]
# 刻度对应字体格式
[label.set_fontname('Times New Roman') for label in labels]

ax.legend()
# 显示图形
plt.show()
