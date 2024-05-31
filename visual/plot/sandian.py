import matplotlib.pyplot as plt
import numpy as np

# 定义数据
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

x = [
     [622.5, 6.1, 193.4, 54.2, 83.5, 28.4, 35.6],
     [194.4, 167.5, 160.3, 240.5, ],
     [143.6, 119.7, 237.7,],
     [242.3, 320.7],
    ]
y = [
     [53.1, 62.0, 60.0, 65.5, 69.7 , 67.3, 74.6],
     [76.5, 76.5, 74.2, 77.7, ],
     [79.6, 82.2, 74.7, ],
     [84.9, 83.7],
     ]

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
markers = ['o', 'p', 'v', 'h']

fig, ax = plt.subplots()
plt.rcParams['savefig.dpi'] = 1000 #图片像素
plt.rcParams['figure.dpi'] = 1000 #分辨率
for i, color in enumerate(colors):
     for j, xx in enumerate(x[i]):
        scale = int(y[i][j]-50)*20
        ax.scatter(x[i][j], y[i][j], c=color, s=scale, label='', alpha=0.8, edgecolors='none',)

bwith = 2.0 #边框宽度设置为2
TK = plt.gca()#获取边框
TK.spines['bottom'].set_linewidth(bwith)
TK.spines['left'].set_linewidth(bwith)
TK.spines['top'].set_linewidth(bwith)
TK.spines['right'].set_linewidth(bwith)

plt.grid(linestyle='--', which='major')

plt.show()
