import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


def compute_mcle(ground_truths, predictions):
    """
    计算平均中心位置误差

    :param ground_truths: 真实边界框列表，每个边界框是一个(x, y, width, height)的元组
    :param predictions: 预测边界框列表，格式与真实边界框相同
    :return: 平均中心位置误差
    """
    errors = []
    for gt, pred in zip(ground_truths, predictions):
        # 计算真实边界框和预测边界框的中心点
        gt_center_x = gt[0] + gt[2] / 2
        gt_center_y = gt[1] + gt[3] / 2
        pred_center_x = pred[0] + pred[2] / 2
        pred_center_y = pred[1] + pred[3] / 2

        # 计算两个中心点之间的欧氏距离
        error = ((gt_center_x - pred_center_x) ** 2 + (gt_center_y - pred_center_y) ** 2) ** 0.5
        errors.append(error/1)

    # 计算所有误差的平均值
    return errors

if __name__ == '__main__':
    name = 'DJI_0034'
    gt_path = '/home/lsw/LSW/projects/tools/visual/real_world/frames/{}/groundtruth_rect.txt'.format(name)
    pred_path = '/home/lsw/LSW/projects/tools/visual/real_world/txt/{}.txt'.format(name)
    gt = np.loadtxt(gt_path, delimiter=',').astype('int_')
    pred = np.loadtxt(pred_path, delimiter='\t').astype('int_')
    mcle = compute_mcle(gt, pred)

    #保存数据
    save_path = '/home/lsw/LSW/projects/tools/visual/real_world/cle/{}.txt'.format(name)
    # np.savetxt(save_path, np.c_[mcle], fmt='%s', delimiter='\t')

    #画线
    y_file = save_path
    y1 = np.loadtxt(y_file, delimiter='\t')
    x = range(0, y1.shape[0])

    plt.figure(figsize=(20.0, 4))
    plt.plot(x, y1, linewidth=4, label='', color='tab:red', linestyle='solid')  # 画图，自变量x放前面
    # 以下为图形设置参数
    plt.legend(frameon=False, loc="upper left", fontsize='large')  # 设置图例无边框，将图例放在左上角
    plt.rcParams['figure.figsize'] = (20.0, 4)  # 图形大小
    plt.rcParams['savefig.dpi'] = 300  # 图片像素
    plt.rcParams['figure.dpi'] = 300  # 分辨率

    font1 = {
            # 'family': 'Arial',
             'weight': 'normal',
             'size': 30,
             }
    plt.xlabel('Frames', font1)  # x轴坐标名称及字体样式
    plt.ylabel('CLE', font1)  # y轴坐标名称及字体样式
    plt.grid(linestyle='--')

    plt.xticks(fontsize=30)  # x轴刻度字体大小
    plt.yticks(fontsize=30)  # y轴刻度字体大小
    plt.xlim(0, len(x))  # X轴范围
    plt.ylim(0, 20)  # 显示y轴范围
    y_major_locator = MultipleLocator(10)
    # 设置图框线粗细
    bwith = 5  # 边框宽度设置为2
    TK = plt.gca()  # 获取边框
    TK.spines['bottom'].set_linewidth(bwith)
    TK.spines['left'].set_linewidth(bwith)
    TK.spines['top'].set_linewidth(bwith)
    TK.spines['right'].set_linewidth(bwith)
    TK.yaxis.set_major_locator(y_major_locator)

    # plt.grid() #显示网格线
    plt.savefig('/home/lsw/LSW/projects/tools/visual/real_world/cle/{}.png'.format(name))
    plt.show()

