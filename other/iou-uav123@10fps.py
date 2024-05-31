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

sequence_info_list = [
    {'name': 'bike1', 'path': 'data_seq/UAV123_10fps/bike1', 'startFrame': 1, 'endFrame': 1029},
    {'name': 'bike2', 'path': 'data_seq/UAV123_10fps/bike2', 'startFrame': 1, 'endFrame': 185},
    {'name': 'bike3', 'path': 'data_seq/UAV123_10fps/bike3', 'startFrame': 1, 'endFrame': 145},
    {'name': 'bird1_1', 'path': 'data_seq/UAV123_10fps/bird1', 'startFrame': 1, 'endFrame': 85},
    {'name': 'bird1_2', 'path': 'data_seq/UAV123_10fps/bird1', 'startFrame': 259, 'endFrame': 493},
    {'name': 'bird1_3', 'path': 'data_seq/UAV123_10fps/bird1', 'startFrame': 525, 'endFrame': 813},
    {'name': 'boat1', 'path': 'data_seq/UAV123_10fps/boat1', 'startFrame': 1, 'endFrame': 301},
    {'name': 'boat2', 'path': 'data_seq/UAV123_10fps/boat2', 'startFrame': 1, 'endFrame': 267},
    {'name': 'boat3', 'path': 'data_seq/UAV123_10fps/boat3', 'startFrame': 1, 'endFrame': 301},
    {'name': 'boat4', 'path': 'data_seq/UAV123_10fps/boat4', 'startFrame': 1, 'endFrame': 185},
    {'name': 'boat5', 'path': 'data_seq/UAV123_10fps/boat5', 'startFrame': 1, 'endFrame': 169},
    {'name': 'boat6', 'path': 'data_seq/UAV123_10fps/boat6', 'startFrame': 1, 'endFrame': 269},
    {'name': 'boat7', 'path': 'data_seq/UAV123_10fps/boat7', 'startFrame': 1, 'endFrame': 179},
    {'name': 'boat8', 'path': 'data_seq/UAV123_10fps/boat8', 'startFrame': 1, 'endFrame': 229},
    {'name': 'boat9', 'path': 'data_seq/UAV123_10fps/boat9', 'startFrame': 1, 'endFrame': 467},
    {'name': 'building1', 'path': 'data_seq/UAV123_10fps/building1', 'startFrame': 1, 'endFrame': 157},
    {'name': 'building2', 'path': 'data_seq/UAV123_10fps/building2', 'startFrame': 1, 'endFrame': 193},
    {'name': 'building3', 'path': 'data_seq/UAV123_10fps/building3', 'startFrame': 1, 'endFrame': 277},
    {'name': 'building4', 'path': 'data_seq/UAV123_10fps/building4', 'startFrame': 1, 'endFrame': 263},
    {'name': 'building5', 'path': 'data_seq/UAV123_10fps/building5', 'startFrame': 1, 'endFrame': 161},
    {'name': 'car1_1', 'path': 'data_seq/UAV123_10fps/car1', 'startFrame': 1, 'endFrame': 251},
    {'name': 'car1_2', 'path': 'data_seq/UAV123_10fps/car1', 'startFrame': 251, 'endFrame': 543},
    {'name': 'car1_3', 'path': 'data_seq/UAV123_10fps/car1', 'startFrame': 543, 'endFrame': 877},
    {'name': 'car2', 'path': 'data_seq/UAV123_10fps/car2', 'startFrame': 1, 'endFrame': 441},
    {'name': 'car3', 'path': 'data_seq/UAV123_10fps/car3', 'startFrame': 1, 'endFrame': 573},
    {'name': 'car4', 'path': 'data_seq/UAV123_10fps/car4', 'startFrame': 1, 'endFrame': 449},
    {'name': 'car5', 'path': 'data_seq/UAV123_10fps/car5', 'startFrame': 1, 'endFrame': 249},
    {'name': 'car6_1', 'path': 'data_seq/UAV123_10fps/car6', 'startFrame': 1, 'endFrame': 163},
    {'name': 'car6_2', 'path': 'data_seq/UAV123_10fps/car6', 'startFrame': 163, 'endFrame': 603},
    {'name': 'car6_3', 'path': 'data_seq/UAV123_10fps/car6', 'startFrame': 603, 'endFrame': 985},
    {'name': 'car6_4', 'path': 'data_seq/UAV123_10fps/car6', 'startFrame': 985, 'endFrame': 1309},
    {'name': 'car6_5', 'path': 'data_seq/UAV123_10fps/car6', 'startFrame': 1309, 'endFrame': 1621},
    {'name': 'car7', 'path': 'data_seq/UAV123_10fps/car7', 'startFrame': 1, 'endFrame': 345},
    {'name': 'car8_1', 'path': 'data_seq/UAV123_10fps/car8', 'startFrame': 1, 'endFrame': 453},
    {'name': 'car8_2', 'path': 'data_seq/UAV123_10fps/car8', 'startFrame': 453, 'endFrame': 859},
    {'name': 'car9', 'path': 'data_seq/UAV123_10fps/car9', 'startFrame': 1, 'endFrame': 627},
    {'name': 'car10', 'path': 'data_seq/UAV123_10fps/car10', 'startFrame': 1, 'endFrame': 469},
    {'name': 'car11', 'path': 'data_seq/UAV123_10fps/car11', 'startFrame': 1, 'endFrame': 113},
    {'name': 'car12', 'path': 'data_seq/UAV123_10fps/car12', 'startFrame': 1, 'endFrame': 167},
    {'name': 'car13', 'path': 'data_seq/UAV123_10fps/car13', 'startFrame': 1, 'endFrame': 139},
    {'name': 'car14', 'path': 'data_seq/UAV123_10fps/car14', 'startFrame': 1, 'endFrame': 443},
    {'name': 'car15', 'path': 'data_seq/UAV123_10fps/car15', 'startFrame': 1, 'endFrame': 157},
    {'name': 'car16_1', 'path': 'data_seq/UAV123_10fps/car16', 'startFrame': 1, 'endFrame': 139},
    {'name': 'car16_2', 'path': 'data_seq/UAV123_10fps/car16', 'startFrame': 139, 'endFrame': 665},
    {'name': 'car17', 'path': 'data_seq/UAV123_10fps/car17', 'startFrame': 1, 'endFrame': 353},
    {'name': 'car18', 'path': 'data_seq/UAV123_10fps/car18', 'startFrame': 1, 'endFrame': 403},
    {'name': 'group1_1', 'path': 'data_seq/UAV123_10fps/group1', 'startFrame': 1, 'endFrame': 445},
    {'name': 'group1_2', 'path': 'data_seq/UAV123_10fps/group1', 'startFrame': 445, 'endFrame': 839},
    {'name': 'group1_3', 'path': 'data_seq/UAV123_10fps/group1', 'startFrame': 839, 'endFrame': 1309},
    {'name': 'group1_4', 'path': 'data_seq/UAV123_10fps/group1', 'startFrame': 1309, 'endFrame': 1625},
    {'name': 'group2_1', 'path': 'data_seq/UAV123_10fps/group2', 'startFrame': 1, 'endFrame': 303},
    {'name': 'group2_2', 'path': 'data_seq/UAV123_10fps/group2', 'startFrame': 303, 'endFrame': 591},
    {'name': 'group2_3', 'path': 'data_seq/UAV123_10fps/group2', 'startFrame': 591, 'endFrame': 895},
    {'name': 'group3_1', 'path': 'data_seq/UAV123_10fps/group3', 'startFrame': 1, 'endFrame': 523},
    {'name': 'group3_2', 'path': 'data_seq/UAV123_10fps/group3', 'startFrame': 523, 'endFrame': 943},
    {'name': 'group3_3', 'path': 'data_seq/UAV123_10fps/group3', 'startFrame': 943, 'endFrame': 1457},
    {'name': 'group3_4', 'path': 'data_seq/UAV123_10fps/group3', 'startFrame': 1457, 'endFrame': 1843},
    {'name': 'person1', 'path': 'data_seq/UAV123_10fps/person1', 'startFrame': 1, 'endFrame': 267},
    {'name': 'person2_1', 'path': 'data_seq/UAV123_10fps/person2', 'startFrame': 1, 'endFrame': 397},
    {'name': 'person2_2', 'path': 'data_seq/UAV123_10fps/person2', 'startFrame': 397, 'endFrame': 875},
    {'name': 'person3', 'path': 'data_seq/UAV123_10fps/person3', 'startFrame': 1, 'endFrame': 215},
    {'name': 'person4_1', 'path': 'data_seq/UAV123_10fps/person4', 'startFrame': 1, 'endFrame': 501},
    {'name': 'person4_2', 'path': 'data_seq/UAV123_10fps/person4', 'startFrame': 501, 'endFrame': 915},
    {'name': 'person5_1', 'path': 'data_seq/UAV123_10fps/person5', 'startFrame': 1, 'endFrame': 293},
    {'name': 'person5_2', 'path': 'data_seq/UAV123_10fps/person5', 'startFrame': 293, 'endFrame': 701},
    {'name': 'person6', 'path': 'data_seq/UAV123_10fps/person6', 'startFrame': 1, 'endFrame': 301},
    {'name': 'person7_1', 'path': 'data_seq/UAV123_10fps/person7', 'startFrame': 1, 'endFrame': 417},
    {'name': 'person7_2', 'path': 'data_seq/UAV123_10fps/person7', 'startFrame': 417, 'endFrame': 689},
    {'name': 'person8_1', 'path': 'data_seq/UAV123_10fps/person8', 'startFrame': 1, 'endFrame': 359},
    {'name': 'person8_2', 'path': 'data_seq/UAV123_10fps/person8', 'startFrame': 359, 'endFrame': 509},
    {'name': 'person9', 'path': 'data_seq/UAV123_10fps/person9', 'startFrame': 1, 'endFrame': 221},
    {'name': 'person10', 'path': 'data_seq/UAV123_10fps/person10', 'startFrame': 1, 'endFrame': 341},
    {'name': 'person11', 'path': 'data_seq/UAV123_10fps/person11', 'startFrame': 1, 'endFrame': 241},
    {'name': 'person12_1', 'path': 'data_seq/UAV123_10fps/person12', 'startFrame': 1, 'endFrame': 201},
    {'name': 'person12_2', 'path': 'data_seq/UAV123_10fps/person12', 'startFrame': 201, 'endFrame': 541},
    {'name': 'person13', 'path': 'data_seq/UAV123_10fps/person13', 'startFrame': 1, 'endFrame': 295},
    {'name': 'person14_1', 'path': 'data_seq/UAV123_10fps/person14', 'startFrame': 1, 'endFrame': 283},
    {'name': 'person14_2', 'path': 'data_seq/UAV123_10fps/person14', 'startFrame': 283, 'endFrame': 605},
    {'name': 'person14_3', 'path': 'data_seq/UAV123_10fps/person14', 'startFrame': 605, 'endFrame': 975},
    {'name': 'person15', 'path': 'data_seq/UAV123_10fps/person15', 'startFrame': 1, 'endFrame': 447},
    {'name': 'person16', 'path': 'data_seq/UAV123_10fps/person16', 'startFrame': 1, 'endFrame': 383},
    {'name': 'person17_1', 'path': 'data_seq/UAV123_10fps/person17', 'startFrame': 1, 'endFrame': 501},
    {'name': 'person17_2', 'path': 'data_seq/UAV123_10fps/person17', 'startFrame': 501, 'endFrame': 783},
    {'name': 'person18', 'path': 'data_seq/UAV123_10fps/person18', 'startFrame': 1, 'endFrame': 465},
    {'name': 'person19_1', 'path': 'data_seq/UAV123_10fps/person19', 'startFrame': 1, 'endFrame': 415},
    {'name': 'person19_2', 'path': 'data_seq/UAV123_10fps/person19', 'startFrame': 415, 'endFrame': 931},
    {'name': 'person19_3', 'path': 'data_seq/UAV123_10fps/person19', 'startFrame': 931, 'endFrame': 1453},
    {'name': 'person20', 'path': 'data_seq/UAV123_10fps/person20', 'startFrame': 1, 'endFrame': 595},
    {'name': 'person21', 'path': 'data_seq/UAV123_10fps/person21', 'startFrame': 1, 'endFrame': 163},
    {'name': 'person22', 'path': 'data_seq/UAV123_10fps/person22', 'startFrame': 1, 'endFrame': 67},
    {'name': 'person23', 'path': 'data_seq/UAV123_10fps/person23', 'startFrame': 1, 'endFrame': 133},
    {'name': 'truck1', 'path': 'data_seq/UAV123_10fps/truck1', 'startFrame': 1, 'endFrame': 155},
    {'name': 'truck2', 'path': 'data_seq/UAV123_10fps/truck2', 'startFrame': 1, 'endFrame': 129},
    {'name': 'truck3', 'path': 'data_seq/UAV123_10fps/truck3', 'startFrame': 1, 'endFrame': 179},
    {'name': 'truck4_1', 'path': 'data_seq/UAV123_10fps/truck4', 'startFrame': 1, 'endFrame': 193},
    {'name': 'truck4_2', 'path': 'data_seq/UAV123_10fps/truck4', 'startFrame': 193, 'endFrame': 421},
    {'name': 'uav1_1', 'path': 'data_seq/UAV123_10fps/uav1', 'startFrame': 1, 'endFrame': 519},
    {'name': 'uav1_2', 'path': 'data_seq/UAV123_10fps/uav1', 'startFrame': 519, 'endFrame': 793},
    {'name': 'uav1_3', 'path': 'data_seq/UAV123_10fps/uav1', 'startFrame': 825, 'endFrame': 1157},
    {'name': 'uav2', 'path': 'data_seq/UAV123_10fps/uav2', 'startFrame': 1, 'endFrame': 45},
    {'name': 'uav3', 'path': 'data_seq/UAV123_10fps/uav3', 'startFrame': 1, 'endFrame': 89},
    {'name': 'uav4', 'path': 'data_seq/UAV123_10fps/uav4', 'startFrame': 1, 'endFrame': 53},
    {'name': 'uav5', 'path': 'data_seq/UAV123_10fps/uav5', 'startFrame': 1, 'endFrame': 47},
    {'name': 'uav6', 'path': 'data_seq/UAV123_10fps/uav6', 'startFrame': 1, 'endFrame': 37},
    {'name': 'uav7', 'path': 'data_seq/UAV123_10fps/uav7', 'startFrame': 1, 'endFrame': 125},
    {'name': 'uav8', 'path': 'data_seq/UAV123_10fps/uav8', 'startFrame': 1, 'endFrame': 101},
    {'name': 'wakeboard1', 'path': 'data_seq/UAV123_10fps/wakeboard1', 'startFrame': 1, 'endFrame': 141},
    {'name': 'wakeboard2', 'path': 'data_seq/UAV123_10fps/wakeboard2', 'startFrame': 1, 'endFrame': 245},
    {'name': 'wakeboard3', 'path': 'data_seq/UAV123_10fps/wakeboard3', 'startFrame': 1, 'endFrame': 275},
    {'name': 'wakeboard4', 'path': 'data_seq/UAV123_10fps/wakeboard4', 'startFrame': 1, 'endFrame': 233},
    {'name': 'wakeboard5', 'path': 'data_seq/UAV123_10fps/wakeboard5', 'startFrame': 1, 'endFrame': 559},
    {'name': 'wakeboard6', 'path': 'data_seq/UAV123_10fps/wakeboard6', 'startFrame': 1, 'endFrame': 389},
    {'name': 'wakeboard7', 'path': 'data_seq/UAV123_10fps/wakeboard7', 'startFrame': 1, 'endFrame': 67},
    {'name': 'wakeboard8', 'path': 'data_seq/UAV123_10fps/wakeboard8', 'startFrame': 1, 'endFrame': 515},
    {'name': 'wakeboard9', 'path': 'data_seq/UAV123_10fps/wakeboard9', 'startFrame': 1, 'endFrame': 119},
    {'name': 'wakeboard10', 'path': 'data_seq/UAV123_10fps/wakeboard10', 'startFrame': 1, 'endFrame': 157},
    {'name': 'car1_s', 'path': 'data_seq/UAV123_10fps/car1_s', 'startFrame': 1, 'endFrame': 492},
    {'name': 'car2_s', 'path': 'data_seq/UAV123_10fps/car2_s', 'startFrame': 1, 'endFrame': 107},
    {'name': 'car3_s', 'path': 'data_seq/UAV123_10fps/car3_s', 'startFrame': 1, 'endFrame': 434},
    {'name': 'car4_s', 'path': 'data_seq/UAV123_10fps/car4_s', 'startFrame': 1, 'endFrame': 277},
    {'name': 'person1_s', 'path': 'data_seq/UAV123_10fps/person1_s', 'startFrame': 1, 'endFrame': 534},
    {'name': 'person2_s', 'path': 'data_seq/UAV123_10fps/person2_s', 'startFrame': 1, 'endFrame': 84},
    {'name': 'person3_s', 'path': 'data_seq/UAV123_10fps/person3_s', 'startFrame': 1, 'endFrame': 169}]
for i in sequence_info_list:
    i['nz'] = 6
    i['ext'] = 'jpg'
    i['anno_path'] = 'anno/UAV123_10fps/' + i['name'] + '.txt'
    i['object_class'] = 'cat'

# sequence_list = []
# for s in sequence_info_list:
#     if s['name'] in ['uav_group1_1']:
#         sequence_list.append(s)


input_ptah = '/home/lsw/LSW/projects/tools/other/input/uav123_10fps'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['TATrack']
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/other/output/uav123_10fps'
data_path = '/home/lsw/data/UAV123@10FPS'

# {"name": "uav_bike1", "path": "data_seq/UAV123/bike1", "startFrame": 1, "endFrame": 3085, "nz": 6,"ext": "jpg",
# "anno_path": "anno/UAV123/bike1.txt", "object_class": "vehicle"},

for j, m in enumerate(sequence_info_list):
    mean_iou = []
    for i, n in enumerate(trackers):
        bbox_file = os.path.join(bbox_path[i], '{}.txt'.format(m['name']))
        bbox = np.loadtxt(bbox_file, delimiter='\t')

        anno_file = '{}/{}'.format(data_path, m['anno_path'])
        anno = np.loadtxt(anno_file, delimiter=',')

        save_dir = '{}/{}'.format(save_path, m['name'])
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        ious = []
        for k in range(1, bbox.shape[0], 1):
            iou = box_iou_xywh(bbox[k], anno[k])
            ious.append(iou)
        mean_iou.append(np.array(ious).mean())
        print(m['name'], mean_iou)
        # with open(os.path.join(save_dir, '{}.txt'.format(n)), 'a') as f:
        #     f.write(str(ious)[1:-1])
        #     f.close()
    # if mean_iou[2] - mean_iou[1] > 0.1:
    #     print(m['name'], mean_iou)






