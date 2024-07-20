import matplotlib.pyplot as plt
import numpy as np

# tracker: DIMP(ICCV19), SiamRPN++(CVPR19), PrDiMP(CVPR20), TransT(CVPR21), KeepTrack(ICCV21), ToMP(CVPR22), OSTrack(ECCV22), CTTrack(AAAI23), ARTrack(CVPR23)

# uav123
x = [
     [51.0 , 57.0 , 53.0 , 55.0 , 43.0 , 24.0 , 13.0 , 68.0 ,30.0 ,13.0 ],
     [265],
    ]
y = [
     [64.3, 61.3, 65.3, 69.1, 68.5, 68.5 , 69.7 , 67.5 ,67.9 ,68.6 ],
     [66.7],
     ]

# dtb70
# x = [
#      [52.0  , 58.0  , 42.0  , 54.0   , 45.0   , 26.0   , 15.0  , 70.0 ,36.0  ,15.0  ],
#      [278.0 ],
#     ]
# y = [
#      [79.2 , 79.9 , 76.4 , 83.6 , 82.1 , 85.6  , 82.9  , 82.7  , 87.5  ,86.0  ],
#      [83.6 ],
#      ]


tracker = ['DIMP(ICCV19)', 'SiamRPN++(CVPR19)', 'PrDiMP(CVPR20)', 'TransT(CVPR21)', 'STARK(ICCV21)', 'ToMP(CVPR22)', 'MixFormer(CVPR22)', 'OSTrack(ECCV22)', 'ARTrack(CVPR23)', 'SeqTrack(CVPR23)', 'Aba-ViTrack++(Ours)']
colors = ['tab:blue', 'tab:red']
markers = ['^', '*']

fig, ax = plt.subplots()
plt.rcParams['savefig.dpi'] = 1000 #图片像素
plt.rcParams['figure.dpi'] = 1000 #分辨率
s = []
for i, color in enumerate(colors):
     for j, xx in enumerate(x[i]):
        scale = i*150 + 150
        alpha = i*0.2 + 0.8
        s.append(ax.scatter(x[i][j], y[i][j], c=color, s=scale, label='', alpha=alpha, edgecolors='black', marker=markers[i]))

s = tuple(list(reversed(s)))
tracker = tuple(list(reversed(tracker)))
bwith = 2.0 #边框宽度设置为2
TK = plt.gca()#获取边框
TK.spines['bottom'].set_linewidth(bwith)
TK.spines['left'].set_linewidth(bwith)
TK.spines['top'].set_linewidth(bwith)
TK.spines['right'].set_linewidth(bwith)
plt.xticks(fontsize=16)  # x轴刻度字体大小
plt.yticks(fontsize=16)  # y轴刻度字体大小
plt.grid(linestyle='--', which='major')

ax.legend(s, tracker, loc = 2, bbox_to_anchor=(1.05, 1), borderaxespad=0)

plt.savefig('/home/lsw/LSW/projects/tools/visual/plot/output/sandian/{}.png'.format(1))
plt.show()


