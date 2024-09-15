import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

# 定义数据
# uav123
# x = [
#      [622.5, 6.1, 193.4, 54.2, 83.5, 28.4, 63.4, 34.2, 57.8, 35.6,],
#      [194.4, 167.5, 160.3, 240.5, 139.6, 255.4,],
#      [143.6, 119.7, 237.7, 184.6,],
#      [203.3, 271.6, 172.5, 187.0, 242.3, 320.7],
#     ]
# y = [
#      [53.1, 62.0, 60.0, 65.5, 69.7 , 67.3 , 66.6, 71.0, 71.6, 74.6,],
#      [76.5, 76.5, 74.2, 77.7, 78.3, 78.5,],
#      [79.6, 82.2, 74.7, 72.6,],
#      [83.4, 81.4, 81.3, 83.9, 84.9, 83.7],
#      ]

# uav123@10fps
x = [
     [623, 6.1, 193, 84, 28.4, 34, 56],
     [194, 160, 119, 140, 34],
     [237, 184, 243,],
     [181, 270],
    ]
y = [
     [40.6 , 58.4, 51.6, 64.0, 62.7, 66.6, 67.1],
     [75.2, 74.9, 78.0, 78.0, 77.3],
     [80.9, 81.0, 83.2],
     [85.0, 85.8],
     ]

colors = ['tab:orange', 'tab:blue', 'tab:green', 'tab:red']
markers = ['o', 'o', 'o', '*']

fig, ax = plt.subplots()
plt.rcParams['savefig.dpi'] = 1000 #图片像素
plt.rcParams['figure.dpi'] = 1000 #分辨率
for i, color in enumerate(colors):
     for j, xx in enumerate(x[i]):
        scale = 150
        alpha = 0.6
        if i == 3:
            scale = (y[i][j]-83)*50 + 180
            alpha = 0.8
        ax.scatter(x[i][j], y[i][j], c=color, s=scale, label='', alpha=alpha, edgecolors='black',marker=markers[i])

plt.xticks(fontsize=14)  # x轴刻度字体大小
plt.yticks(fontsize=14)  # y轴刻度字体大小
bwith = 2.0 #边框宽度设置为2
TK = plt.gca()#获取边框
TK.spines['bottom'].set_linewidth(bwith)
TK.spines['left'].set_linewidth(bwith)
TK.spines['top'].set_linewidth(bwith)
TK.spines['right'].set_linewidth(bwith)
plt.xlim(0, 630)  # X轴范围
plt.ylim(39, 90)  # 显示y轴范围
y_major_locator = MultipleLocator(10)
x_major_locator = MultipleLocator(50)
plt.grid(linestyle='', which='major')
TK.yaxis.set_major_locator(y_major_locator)
TK.xaxis.set_major_locator(x_major_locator)


plt.show()
