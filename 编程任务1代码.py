import numpy as np
import numpy as nan
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


folder_path = "C:/Users/28166/Desktop/环科院培训/编程任务一/Beijing/Y2014"  # 文件夹路径

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # 仅处理txt文件
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            lines = file.readlines()
        with open(file_path, "w") as file:
            for line in lines:
                line = line.replace("Y", "")  # 删除Y字符（大小写敏感）
                file.write(line)

totaldata = []

# 遍历根目录下的所有文件夹和文件
for root, dirs, files in os.walk('C:/Users/28166/Desktop/环科院培训/编程任务一/Beijing'):  # 在beijing这个文件夹疯狂遍历
    # 遍历二级文件夹
    for dir in dirs:    # dir是Y2013文件夹
        # 拼接二级文件夹路径
        dir_path = os.path.join(root, dir)
        yeardata = []  # 存放每个月的平均值，放12个站点1年的数据，共144个数
        # 遍历二级文件夹下的所有文件
        for file in os.listdir(dir_path):
            # 拼接文件路径
            file_path = os.path.join(dir_path, file)  # beijing-Y2013-接着12个文本文件
            # 处理文件
            i = 1
            count = 0
            emonth = 0
            monthdata = []  # 一个月的数据
            with open(file_path, 'r') as f:
                # 逐个读取文件
                '''content = f.read()
                print(content)'''
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
                    if time_obj.month == i:
                        if data != -999.000:
                            count = count + 1
                        if data == -999.000:
                            data = np.nan
                        monthdata.append(data)
                        if time_obj.month == 12 and time_obj.day == 31:
                                if count < 20:
                                    emonth = np.nan
                                else:
                                    emonth = np.nanmean(monthdata)  # 算每个月的平均值
                                yeardata.append(emonth)
                    else:
                        if count < 20:
                            emonth = np.nan
                        else:
                            emonth = np.nanmean(monthdata)
                        yeardata.append(emonth)
                        monthdata.clear()
                        count = 0
                        if data != -999.000:
                            count = count + 1
                        if data == -999.000:
                            data = np.nan
                        monthdata.append(data)
                        i = i + 1
        # 定义新列表
        new_list = []   #

        # 循环遍历长列表
        for i in range(0, len(yeardata), 12):
            # 取出每间隔12个数据的子列表
            sub_list = yeardata[i:i+12]
            # 对子列表进行求和
            sum_value = np.nanmean(sub_list)
            # 将求和结果存入新列表中
            new_list.append(sum_value)
        # 输出新列表
        print(new_list)
        totaldata.append(new_list)

print(totaldata)

# 二维列表变成一维
totaldata = [num for row in totaldata for num in row]
print(totaldata)
print(len(totaldata))

#画图
time_index = pd.date_range('01/2013', '12/2021', freq='MS')
y = totaldata
# 创建画布和子图
fig, ax = plt.subplots()
# 设置横轴坐标格式为年月
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
# 绘制折线图
ax.plot(time_index, y, 'o-')
# 设置横轴坐标刻度
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

# 设置横纵坐标的名称以及对应字体格式
font2 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 14, }
plt.xlabel('Year-Month', font2)
plt.ylabel('PM25(ug/m3)', font2)

# 横纵轴刻度一起设置
labels = ax.get_xticklabels() + ax.get_yticklabels()
# 设置横轴刻度旋转程度为30度
[label.set_rotation(75) for label in ax.get_xticklabels()]
# 刻度对应字体格式
[label.set_fontname('Times New Roman') for label in labels]

plt.title('Monthly average PM2.5 concentration variation curve at 12 stations in Beijing', fontdict={'family': 'Times New Roman', 'size': 20, })

# 显示图形
plt.show()