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
    {"name": "uav_bike1", "path": "data_seq/UAV123/bike1", "startFrame": 1, "endFrame": 3085, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bike1.txt", "object_class": "vehicle"},
    {"name": "uav_bike2", "path": "data_seq/UAV123/bike2", "startFrame": 1, "endFrame": 553, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bike2.txt", "object_class": "vehicle"},
    {"name": "uav_bike3", "path": "data_seq/UAV123/bike3", "startFrame": 1, "endFrame": 433, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bike3.txt", "object_class": "vehicle"},
    {"name": "uav_bird1_1", "path": "data_seq/UAV123/bird1", "startFrame": 1, "endFrame": 253, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bird1_1.txt", "object_class": "bird"},
    {"name": "uav_bird1_2", "path": "data_seq/UAV123/bird1", "startFrame": 775, "endFrame": 1477, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bird1_2.txt", "object_class": "bird"},
    {"name": "uav_bird1_3", "path": "data_seq/UAV123/bird1", "startFrame": 1573, "endFrame": 2437, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/bird1_3.txt", "object_class": "bird"},
    {"name": "uav_boat1", "path": "data_seq/UAV123/boat1", "startFrame": 1, "endFrame": 901, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat1.txt", "object_class": "vessel"},
    {"name": "uav_boat2", "path": "data_seq/UAV123/boat2", "startFrame": 1, "endFrame": 799, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat2.txt", "object_class": "vessel"},
    {"name": "uav_boat3", "path": "data_seq/UAV123/boat3", "startFrame": 1, "endFrame": 901, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat3.txt", "object_class": "vessel"},
    {"name": "uav_boat4", "path": "data_seq/UAV123/boat4", "startFrame": 1, "endFrame": 553, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat4.txt", "object_class": "vessel"},
    {"name": "uav_boat5", "path": "data_seq/UAV123/boat5", "startFrame": 1, "endFrame": 505, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat5.txt", "object_class": "vessel"},
    {"name": "uav_boat6", "path": "data_seq/UAV123/boat6", "startFrame": 1, "endFrame": 805, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat6.txt", "object_class": "vessel"},
    {"name": "uav_boat7", "path": "data_seq/UAV123/boat7", "startFrame": 1, "endFrame": 535, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat7.txt", "object_class": "vessel"},
    {"name": "uav_boat8", "path": "data_seq/UAV123/boat8", "startFrame": 1, "endFrame": 685, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat8.txt", "object_class": "vessel"},
    {"name": "uav_boat9", "path": "data_seq/UAV123/boat9", "startFrame": 1, "endFrame": 1399, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/boat9.txt", "object_class": "vessel"},
    {"name": "uav_building1", "path": "data_seq/UAV123/building1", "startFrame": 1, "endFrame": 469, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/building1.txt", "object_class": "other"},
    {"name": "uav_building2", "path": "data_seq/UAV123/building2", "startFrame": 1, "endFrame": 577, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/building2.txt", "object_class": "other"},
    {"name": "uav_building3", "path": "data_seq/UAV123/building3", "startFrame": 1, "endFrame": 829, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/building3.txt", "object_class": "other"},
    {"name": "uav_building4", "path": "data_seq/UAV123/building4", "startFrame": 1, "endFrame": 787, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/building4.txt", "object_class": "other"},
    {"name": "uav_building5", "path": "data_seq/UAV123/building5", "startFrame": 1, "endFrame": 481, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/building5.txt", "object_class": "other"},
    {"name": "uav_car1_1", "path": "data_seq/UAV123/car1", "startFrame": 1, "endFrame": 751, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car1_1.txt", "object_class": "car"},
    {"name": "uav_car1_2", "path": "data_seq/UAV123/car1", "startFrame": 751, "endFrame": 1627, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car1_2.txt", "object_class": "car"},
    {"name": "uav_car1_3", "path": "data_seq/UAV123/car1", "startFrame": 1627, "endFrame": 2629, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car1_3.txt", "object_class": "car"},
    {"name": "uav_car10", "path": "data_seq/UAV123/car10", "startFrame": 1, "endFrame": 1405, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car10.txt", "object_class": "car"},
    {"name": "uav_car11", "path": "data_seq/UAV123/car11", "startFrame": 1, "endFrame": 337, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car11.txt", "object_class": "car"},
    {"name": "uav_car12", "path": "data_seq/UAV123/car12", "startFrame": 1, "endFrame": 499, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car12.txt", "object_class": "car"},
    {"name": "uav_car13", "path": "data_seq/UAV123/car13", "startFrame": 1, "endFrame": 415, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car13.txt", "object_class": "car"},
    {"name": "uav_car14", "path": "data_seq/UAV123/car14", "startFrame": 1, "endFrame": 1327, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car14.txt", "object_class": "car"},
    {"name": "uav_car15", "path": "data_seq/UAV123/car15", "startFrame": 1, "endFrame": 469, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car15.txt", "object_class": "car"},
    {"name": "uav_car16_1", "path": "data_seq/UAV123/car16", "startFrame": 1, "endFrame": 415, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car16_1.txt", "object_class": "car"},
    {"name": "uav_car16_2", "path": "data_seq/UAV123/car16", "startFrame": 415, "endFrame": 1993, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car16_2.txt", "object_class": "car"},
    {"name": "uav_car17", "path": "data_seq/UAV123/car17", "startFrame": 1, "endFrame": 1057, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car17.txt", "object_class": "car"},
    {"name": "uav_car18", "path": "data_seq/UAV123/car18", "startFrame": 1, "endFrame": 1207, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car18.txt", "object_class": "car"},
    {"name": "uav_car1_s", "path": "data_seq/UAV123/car1_s", "startFrame": 1, "endFrame": 1475, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car1_s.txt", "object_class": "car"},
    {"name": "uav_car2", "path": "data_seq/UAV123/car2", "startFrame": 1, "endFrame": 1321, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car2.txt", "object_class": "car"},
    {"name": "uav_car2_s", "path": "data_seq/UAV123/car2_s", "startFrame": 1, "endFrame": 320, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car2_s.txt", "object_class": "car"},
    {"name": "uav_car3", "path": "data_seq/UAV123/car3", "startFrame": 1, "endFrame": 1717, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car3.txt", "object_class": "car"},
    {"name": "uav_car3_s", "path": "data_seq/UAV123/car3_s", "startFrame": 1, "endFrame": 1300, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car3_s.txt", "object_class": "car"},
    {"name": "uav_car4", "path": "data_seq/UAV123/car4", "startFrame": 1, "endFrame": 1345, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car4.txt", "object_class": "car"},
    {"name": "uav_car4_s", "path": "data_seq/UAV123/car4_s", "startFrame": 1, "endFrame": 830, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car4_s.txt", "object_class": "car"},
    {"name": "uav_car5", "path": "data_seq/UAV123/car5", "startFrame": 1, "endFrame": 745, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car5.txt", "object_class": "car"},
    {"name": "uav_car6_1", "path": "data_seq/UAV123/car6", "startFrame": 1, "endFrame": 487, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car6_1.txt", "object_class": "car"},
    {"name": "uav_car6_2", "path": "data_seq/UAV123/car6", "startFrame": 487, "endFrame": 1807, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car6_2.txt", "object_class": "car"},
    {"name": "uav_car6_3", "path": "data_seq/UAV123/car6", "startFrame": 1807, "endFrame": 2953, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car6_3.txt", "object_class": "car"},
    {"name": "uav_car6_4", "path": "data_seq/UAV123/car6", "startFrame": 2953, "endFrame": 3925, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car6_4.txt", "object_class": "car"},
    {"name": "uav_car6_5", "path": "data_seq/UAV123/car6", "startFrame": 3925, "endFrame": 4861, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car6_5.txt", "object_class": "car"},
    {"name": "uav_car7", "path": "data_seq/UAV123/car7", "startFrame": 1, "endFrame": 1033, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car7.txt", "object_class": "car"},
    {"name": "uav_car8_1", "path": "data_seq/UAV123/car8", "startFrame": 1, "endFrame": 1357, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car8_1.txt", "object_class": "car"},
    {"name": "uav_car8_2", "path": "data_seq/UAV123/car8", "startFrame": 1357, "endFrame": 2575, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car8_2.txt", "object_class": "car"},
    {"name": "uav_car9", "path": "data_seq/UAV123/car9", "startFrame": 1, "endFrame": 1879, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/car9.txt", "object_class": "car"},
    {"name": "uav_group1_1", "path": "data_seq/UAV123/group1", "startFrame": 1, "endFrame": 1333, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group1_1.txt", "object_class": "person"},
    {"name": "uav_group1_2", "path": "data_seq/UAV123/group1", "startFrame": 1333, "endFrame": 2515, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group1_2.txt", "object_class": "person"},
    {"name": "uav_group1_3", "path": "data_seq/UAV123/group1", "startFrame": 2515, "endFrame": 3925, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group1_3.txt", "object_class": "person"},
    {"name": "uav_group1_4", "path": "data_seq/UAV123/group1", "startFrame": 3925, "endFrame": 4873, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group1_4.txt", "object_class": "person"},
    {"name": "uav_group2_1", "path": "data_seq/UAV123/group2", "startFrame": 1, "endFrame": 907, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group2_1.txt", "object_class": "person"},
    {"name": "uav_group2_2", "path": "data_seq/UAV123/group2", "startFrame": 907, "endFrame": 1771, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group2_2.txt", "object_class": "person"},
    {"name": "uav_group2_3", "path": "data_seq/UAV123/group2", "startFrame": 1771, "endFrame": 2683, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group2_3.txt", "object_class": "person"},
    {"name": "uav_group3_1", "path": "data_seq/UAV123/group3", "startFrame": 1, "endFrame": 1567, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group3_1.txt", "object_class": "person"},
    {"name": "uav_group3_2", "path": "data_seq/UAV123/group3", "startFrame": 1567, "endFrame": 2827, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group3_2.txt", "object_class": "person"},
    {"name": "uav_group3_3", "path": "data_seq/UAV123/group3", "startFrame": 2827, "endFrame": 4369, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group3_3.txt", "object_class": "person"},
    {"name": "uav_group3_4", "path": "data_seq/UAV123/group3", "startFrame": 4369, "endFrame": 5527, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/group3_4.txt", "object_class": "person"},
    {"name": "uav_person1", "path": "data_seq/UAV123/person1", "startFrame": 1, "endFrame": 799, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person1.txt", "object_class": "person"},
    {"name": "uav_person10", "path": "data_seq/UAV123/person10", "startFrame": 1, "endFrame": 1021, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person10.txt", "object_class": "person"},
    {"name": "uav_person11", "path": "data_seq/UAV123/person11", "startFrame": 1, "endFrame": 721, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person11.txt", "object_class": "person"},
    {"name": "uav_person12_1", "path": "data_seq/UAV123/person12", "startFrame": 1, "endFrame": 601, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person12_1.txt", "object_class": "person"},
    {"name": "uav_person12_2", "path": "data_seq/UAV123/person12", "startFrame": 601, "endFrame": 1621, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person12_2.txt", "object_class": "person"},
    {"name": "uav_person13", "path": "data_seq/UAV123/person13", "startFrame": 1, "endFrame": 883, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person13.txt", "object_class": "person"},
    {"name": "uav_person14_1", "path": "data_seq/UAV123/person14", "startFrame": 1, "endFrame": 847, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person14_1.txt", "object_class": "person"},
    {"name": "uav_person14_2", "path": "data_seq/UAV123/person14", "startFrame": 847, "endFrame": 1813, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person14_2.txt", "object_class": "person"},
    {"name": "uav_person14_3", "path": "data_seq/UAV123/person14", "startFrame": 1813, "endFrame": 2923,
     "nz": 6, "ext": "jpg", "anno_path": "anno/UAV123/person14_3.txt", "object_class": "person"},
    {"name": "uav_person15", "path": "data_seq/UAV123/person15", "startFrame": 1, "endFrame": 1339, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person15.txt", "object_class": "person"},
    {"name": "uav_person16", "path": "data_seq/UAV123/person16", "startFrame": 1, "endFrame": 1147, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person16.txt", "object_class": "person"},
    {"name": "uav_person17_1", "path": "data_seq/UAV123/person17", "startFrame": 1, "endFrame": 1501, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person17_1.txt", "object_class": "person"},
    {"name": "uav_person17_2", "path": "data_seq/UAV123/person17", "startFrame": 1501, "endFrame": 2347,
     "nz": 6, "ext": "jpg", "anno_path": "anno/UAV123/person17_2.txt", "object_class": "person"},
    {"name": "uav_person18", "path": "data_seq/UAV123/person18", "startFrame": 1, "endFrame": 1393, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person18.txt", "object_class": "person"},
    {"name": "uav_person19_1", "path": "data_seq/UAV123/person19", "startFrame": 1, "endFrame": 1243, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person19_1.txt", "object_class": "person"},
    {"name": "uav_person19_2", "path": "data_seq/UAV123/person19", "startFrame": 1243, "endFrame": 2791,
     "nz": 6, "ext": "jpg", "anno_path": "anno/UAV123/person19_2.txt", "object_class": "person"},
    {"name": "uav_person19_3", "path": "data_seq/UAV123/person19", "startFrame": 2791, "endFrame": 4357,
     "nz": 6, "ext": "jpg", "anno_path": "anno/UAV123/person19_3.txt", "object_class": "person"},
    {"name": "uav_person1_s", "path": "data_seq/UAV123/person1_s", "startFrame": 1, "endFrame": 1600, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person1_s.txt", "object_class": "person"},
    {"name": "uav_person2_1", "path": "data_seq/UAV123/person2", "startFrame": 1, "endFrame": 1189, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person2_1.txt", "object_class": "person"},
    {"name": "uav_person2_2", "path": "data_seq/UAV123/person2", "startFrame": 1189, "endFrame": 2623, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person2_2.txt", "object_class": "person"},
    {"name": "uav_person20", "path": "data_seq/UAV123/person20", "startFrame": 1, "endFrame": 1783, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person20.txt", "object_class": "person"},
    {"name": "uav_person21", "path": "data_seq/UAV123/person21", "startFrame": 1, "endFrame": 487, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person21.txt", "object_class": "person"},
    {"name": "uav_person22", "path": "data_seq/UAV123/person22", "startFrame": 1, "endFrame": 199, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person22.txt", "object_class": "person"},
    {"name": "uav_person23", "path": "data_seq/UAV123/person23", "startFrame": 1, "endFrame": 397, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person23.txt", "object_class": "person"},
    {"name": "uav_person2_s", "path": "data_seq/UAV123/person2_s", "startFrame": 1, "endFrame": 250, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person2_s.txt", "object_class": "person"},
    {"name": "uav_person3", "path": "data_seq/UAV123/person3", "startFrame": 1, "endFrame": 643, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person3.txt", "object_class": "person"},
    {"name": "uav_person3_s", "path": "data_seq/UAV123/person3_s", "startFrame": 1, "endFrame": 505, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person3_s.txt", "object_class": "person"},
    {"name": "uav_person4_1", "path": "data_seq/UAV123/person4", "startFrame": 1, "endFrame": 1501, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person4_1.txt", "object_class": "person"},
    {"name": "uav_person4_2", "path": "data_seq/UAV123/person4", "startFrame": 1501, "endFrame": 2743, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person4_2.txt", "object_class": "person"},
    {"name": "uav_person5_1", "path": "data_seq/UAV123/person5", "startFrame": 1, "endFrame": 877, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person5_1.txt", "object_class": "person"},
    {"name": "uav_person5_2", "path": "data_seq/UAV123/person5", "startFrame": 877, "endFrame": 2101, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person5_2.txt", "object_class": "person"},
    {"name": "uav_person6", "path": "data_seq/UAV123/person6", "startFrame": 1, "endFrame": 901, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person6.txt", "object_class": "person"},
    {"name": "uav_person7_1", "path": "data_seq/UAV123/person7", "startFrame": 1, "endFrame": 1249, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person7_1.txt", "object_class": "person"},
    {"name": "uav_person7_2", "path": "data_seq/UAV123/person7", "startFrame": 1249, "endFrame": 2065, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person7_2.txt", "object_class": "person"},
    {"name": "uav_person8_1", "path": "data_seq/UAV123/person8", "startFrame": 1, "endFrame": 1075, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person8_1.txt", "object_class": "person"},
    {"name": "uav_person8_2", "path": "data_seq/UAV123/person8", "startFrame": 1075, "endFrame": 1525, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person8_2.txt", "object_class": "person"},
    {"name": "uav_person9", "path": "data_seq/UAV123/person9", "startFrame": 1, "endFrame": 661, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/person9.txt", "object_class": "person"},
    {"name": "uav_truck1", "path": "data_seq/UAV123/truck1", "startFrame": 1, "endFrame": 463, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/truck1.txt", "object_class": "truck"},
    {"name": "uav_truck2", "path": "data_seq/UAV123/truck2", "startFrame": 1, "endFrame": 385, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/truck2.txt", "object_class": "truck"},
    {"name": "uav_truck3", "path": "data_seq/UAV123/truck3", "startFrame": 1, "endFrame": 535, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/truck3.txt", "object_class": "truck"},
    {"name": "uav_truck4_1", "path": "data_seq/UAV123/truck4", "startFrame": 1, "endFrame": 577, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/truck4_1.txt", "object_class": "truck"},
    {"name": "uav_truck4_2", "path": "data_seq/UAV123/truck4", "startFrame": 577, "endFrame": 1261, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/truck4_2.txt", "object_class": "truck"},
    {"name": "uav_uav1_1", "path": "data_seq/UAV123/uav1", "startFrame": 1, "endFrame": 1555, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav1_1.txt", "object_class": "aircraft"},
    {"name": "uav_uav1_2", "path": "data_seq/UAV123/uav1", "startFrame": 1555, "endFrame": 2377, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav1_2.txt", "object_class": "aircraft"},
    {"name": "uav_uav1_3", "path": "data_seq/UAV123/uav1", "startFrame": 2473, "endFrame": 3469, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav1_3.txt", "object_class": "aircraft"},
    {"name": "uav_uav2", "path": "data_seq/UAV123/uav2", "startFrame": 1, "endFrame": 133, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav2.txt", "object_class": "aircraft"},
    {"name": "uav_uav3", "path": "data_seq/UAV123/uav3", "startFrame": 1, "endFrame": 265, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav3.txt", "object_class": "aircraft"},
    {"name": "uav_uav4", "path": "data_seq/UAV123/uav4", "startFrame": 1, "endFrame": 157, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav4.txt", "object_class": "aircraft"},
    {"name": "uav_uav5", "path": "data_seq/UAV123/uav5", "startFrame": 1, "endFrame": 139, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav5.txt", "object_class": "aircraft"},
    {"name": "uav_uav6", "path": "data_seq/UAV123/uav6", "startFrame": 1, "endFrame": 109, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav6.txt", "object_class": "aircraft"},
    {"name": "uav_uav7", "path": "data_seq/UAV123/uav7", "startFrame": 1, "endFrame": 373, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav7.txt", "object_class": "aircraft"},
    {"name": "uav_uav8", "path": "data_seq/UAV123/uav8", "startFrame": 1, "endFrame": 301, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/uav8.txt", "object_class": "aircraft"},
    {"name": "uav_wakeboard1", "path": "data_seq/UAV123/wakeboard1", "startFrame": 1, "endFrame": 421, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard1.txt", "object_class": "person"},
    {"name": "uav_wakeboard10", "path": "data_seq/UAV123/wakeboard10", "startFrame": 1, "endFrame": 469,
     "nz": 6, "ext": "jpg", "anno_path": "anno/UAV123/wakeboard10.txt", "object_class": "person"},
    {"name": "uav_wakeboard2", "path": "data_seq/UAV123/wakeboard2", "startFrame": 1, "endFrame": 733, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard2.txt", "object_class": "person"},
    {"name": "uav_wakeboard3", "path": "data_seq/UAV123/wakeboard3", "startFrame": 1, "endFrame": 823, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard3.txt", "object_class": "person"},
    {"name": "uav_wakeboard4", "path": "data_seq/UAV123/wakeboard4", "startFrame": 1, "endFrame": 697, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard4.txt", "object_class": "person"},
    {"name": "uav_wakeboard5", "path": "data_seq/UAV123/wakeboard5", "startFrame": 1, "endFrame": 1675, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard5.txt", "object_class": "person"},
    {"name": "uav_wakeboard6", "path": "data_seq/UAV123/wakeboard6", "startFrame": 1, "endFrame": 1165, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard6.txt", "object_class": "person"},
    {"name": "uav_wakeboard7", "path": "data_seq/UAV123/wakeboard7", "startFrame": 1, "endFrame": 199, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard7.txt", "object_class": "person"},
    {"name": "uav_wakeboard8", "path": "data_seq/UAV123/wakeboard8", "startFrame": 1, "endFrame": 1543, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard8.txt", "object_class": "person"},
    {"name": "uav_wakeboard9", "path": "data_seq/UAV123/wakeboard9", "startFrame": 1, "endFrame": 355, "nz": 6,
     "ext": "jpg", "anno_path": "anno/UAV123/wakeboard9.txt", "object_class": "person"}
]

# sequence_list = []
# for s in sequence_info_list:
#     if s['name'] in ['uav_group1_1']:
#         sequence_list.append(s)


input_ptah = '/home/lsw/LSW/projects/tools/visual/bbox/input/uav123'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['SiamAPN', 'HiFT', 'TCTrack', 'AVTrack', 'Aba-ViTrack', 'Aba-ViTrack++']
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/other/output/uav123'
data_path = '/home/lsw/data/UAV123'

# {"name": "uav_bike1", "path": "data_seq/UAV123/bike1", "startFrame": 1, "endFrame": 3085, "nz": 6,"ext": "jpg",
# "anno_path": "anno/UAV123/bike1.txt", "object_class": "vehicle"},

for j, m in enumerate(sequence_info_list):
    mean_iou = []
    for i, n in enumerate(trackers):
        bbox_file = os.path.join(bbox_path[i], '{}.txt'.format(m['name'][4:]))
        try:
            bbox = np.loadtxt(bbox_file, delimiter='\t')
        except:
            continue

        anno_file = '{}/{}'.format(data_path, m['anno_path'])
        anno = np.loadtxt(anno_file, delimiter=',')

        save_dir = '{}/{}'.format(save_path, m['name'][4:])
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







