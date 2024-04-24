import numpy as np
import matplotlib.pyplot as plt

# Data for plotting

# uav_person3_s, uav_boat5
# boat-12, guitar-16, train-11

dataset = 'lasot'
name = 'boat-12'
y1_file = '/home/lsw/LSW/projects/tools/other/output/{}/{}/{}-good.txt'.format(dataset, name, dataset)
y2_file = '/home/lsw/LSW/projects/tools/other/output/{}/{}/{}-bad2.txt'.format(dataset, name, dataset)
y1 = np.loadtxt(y1_file, delimiter=',')
y2 = np.loadtxt(y2_file, delimiter=',')
x = range(0, y1.shape[0])

plt.figure(figsize=(30.0, 4))
plt.plot(x,y1,linewidth =3, label = '',color='tab:orange', linestyle='solid') #画图，自变量x放前面
plt.plot(x,y2,linewidth =3, label = '',color='tab:blue', linestyle='solid') #画图，自变量x放前面
#以下为图形设置参数
plt.legend(frameon=False,loc="upper left",fontsize='large') #设置图例无边框，将图例放在左上角
plt.rcParams['figure.figsize']=(30.0,4) #图形大小
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率
# 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
# 指定dpi=200，图片尺寸为 1200*800
# 指定dpi=300，图片尺寸为 1800*1200
# 设置figsize可以在不改变分辨率情况下改变比例

font1 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 30,
}
plt.xlabel('frame',font1) #x轴坐标名称及字体样式
plt.ylabel('iou',font1) #y轴坐标名称及字体样式
#插入文本框
# plt.text(-1, 30,'(a)',fontsize=18) #在图中添加文本
plt.grid(linestyle='--')

plt.xticks(fontsize=20) #x轴刻度字体大小
plt.yticks(fontsize=20) #y轴刻度字体大小
plt.xlim(0, len(x))#X轴范围
plt.ylim(0,1)#显示y轴范围

#设置图框线粗细
bwith = 2.5 #边框宽度设置为2
TK = plt.gca()#获取边框
TK.spines['bottom'].set_linewidth(bwith)
TK.spines['left'].set_linewidth(bwith)
TK.spines['top'].set_linewidth(bwith)
TK.spines['right'].set_linewidth(bwith)

#plt.grid() #显示网格线
plt.savefig('/home/lsw/LSW/projects/tools/visual/plot/output/zhexian/{}.png'.format(name))
plt.show()
