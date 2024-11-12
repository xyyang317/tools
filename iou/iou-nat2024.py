def box_iou_xywh(box1, box2):
    # 获取box1左上角的坐标
    x1min, y1min = box1[0] , box1[1]
    # 获取box1右下角的坐标
    x1max, y1max = box1[0] + box1[2], box1[1] + box1[3]
    # 获取box1的面积
    s1 = box1[2] * box1[3]

    # 获取box2左上角的坐标
    x2min, y2min = box2[0], box2[1]
    # 获取box2右下角的坐标
    x2max, y2max = box2[0] + box2[2] , box2[1] + box2[3]
    # 获取box2的面积
    s2 = box2[2] * box2[3]

    # 计算相交矩形框的坐标
    xmin = np.maximum(x1min, x2min)  # 左上角的横坐标
    ymin = np.maximum(y1min, y2min)  # 左上角的纵坐标
    xmax = np.minimum(x1max, x2max)  # 右下角的横坐标
    ymax = np.minimum(y1max, y2max)  # 右下角的纵坐标

    inter_h = np.maximum(ymax - ymin, 0.)
    inter_w = np.maximum(xmax - xmin, 0.)
    intersection = inter_h * inter_w

    union = s1 + s2 - intersection
    iou = intersection / union
    return iou




import glob
import os
import random

import cv2
import numpy as np
from tqdm import tqdm

sequence_info_list = os.listdir('/home/lsw/data/NAT2024-1/data_seq')
input_ptah = '/home/lsw/LSW/projects/tools/iou/input/nat2024'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['MambaNUT', 'UDAT-BAN', 'Sam-DA', 'DCPT', 'TCTrack', 'Aba-ViTrack', 'AVTrack']
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/iou/output/nat2024'
data_path = '/home/lsw/data/NAT2024-1'

# {"name": "uav_bike1", "path": "data_seq/UAV123/bike1", "startFrame": 1, "endFrame": 3085, "nz": 6,"ext": "jpg",
# "anno_path": "anno/UAV123/bike1.txt", "object_class": "vehicle"},

for j, m in enumerate(sequence_info_list):
    mean_iou = []
    for i, n in enumerate(trackers):
        bbox_file = os.path.join(bbox_path[i], '{}.txt'.format(m))
        bbox = np.loadtxt(bbox_file, delimiter='\t')

        anno_file = '{}/anno/{}.txt'.format(data_path, m)
        anno = np.loadtxt(anno_file, delimiter=',')

        save_dir = '{}/{}'.format(save_path, m)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        ious = []
        for k in range(1, bbox.shape[0], 1):
            iou = box_iou_xywh(bbox[k], anno[k])
            ious.append(iou)
        mean_iou.append(np.array(ious).mean())
    print(m, mean_iou)
        # with open(os.path.join(save_dir, '{}.txt'.format(n)), 'a') as f:
        #     f.write(str(ious)[1:-1])
        #     f.close()
    # if mean_iou[2] - mean_iou[1] > 0.1:
    #     print(m['name'], mean_iou)





# L07001,L05011,L05005,L05015,L03001,L05017,L02001,L06002,L05016,L09002

