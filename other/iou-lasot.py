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

sequence_list = ['airplane-1',
                 'airplane-9',
                 'airplane-13',
                 'airplane-15',
                 'basketball-1',
                 'basketball-6',
                 'basketball-7',
                 'basketball-11',
                 'bear-2',
                 'bear-4',
                 'bear-6',
                 'bear-17',
                 'bicycle-2',
                 'bicycle-7',
                 'bicycle-9',
                 'bicycle-18',
                 'bird-2',
                 'bird-3',
                 'bird-15',
                 'bird-17',
                 'boat-3',
                 'boat-4',
                 'boat-12',
                 'boat-17',
                 'book-3',
                 'book-10',
                 'book-11',
                 'book-19',
                 'bottle-1',
                 'bottle-12',
                 'bottle-14',
                 'bottle-18',
                 'bus-2',
                 'bus-5',
                 'bus-17',
                 'bus-19',
                 'car-2',
                 'car-6',
                 'car-9',
                 'car-17',
                 'cat-1',
                 'cat-3',
                 'cat-18',
                 'cat-20',
                 'cattle-2',
                 'cattle-7',
                 'cattle-12',
                 'cattle-13',
                 'spider-14',
                 'spider-16',
                 'spider-18',
                 'spider-20',
                 'coin-3',
                 'coin-6',
                 'coin-7',
                 'coin-18',
                 'crab-3',
                 'crab-6',
                 'crab-12',
                 'crab-18',
                 'surfboard-12',
                 'surfboard-4',
                 'surfboard-5',
                 'surfboard-8',
                 'cup-1',
                 'cup-4',
                 'cup-7',
                 'cup-17',
                 'deer-4',
                 'deer-8',
                 'deer-10',
                 'deer-14',
                 'dog-1',
                 'dog-7',
                 'dog-15',
                 'dog-19',
                 'guitar-3',
                 'guitar-8',
                 'guitar-10',
                 'guitar-16',
                 'person-1',
                 'person-5',
                 'person-10',
                 'person-12',
                 'pig-2',
                 'pig-10',
                 'pig-13',
                 'pig-18',
                 'rubicCube-1',
                 'rubicCube-6',
                 'rubicCube-14',
                 'rubicCube-19',
                 'swing-10',
                 'swing-14',
                 'swing-17',
                 'swing-20',
                 'drone-13',
                 'drone-15',
                 'drone-2',
                 'drone-7',
                 'pool-12',
                 'pool-15',
                 'pool-3',
                 'pool-7',
                 'rabbit-10',
                 'rabbit-13',
                 'rabbit-17',
                 'rabbit-19',
                 'racing-10',
                 'racing-15',
                 'racing-16',
                 'racing-20',
                 'robot-1',
                 'robot-19',
                 'robot-5',
                 'robot-8',
                 'sepia-13',
                 'sepia-16',
                 'sepia-6',
                 'sepia-8',
                 'sheep-3',
                 'sheep-5',
                 'sheep-7',
                 'sheep-9',
                 'skateboard-16',
                 'skateboard-19',
                 'skateboard-3',
                 'skateboard-8',
                 'tank-14',
                 'tank-16',
                 'tank-6',
                 'tank-9',
                 'tiger-12',
                 'tiger-18',
                 'tiger-4',
                 'tiger-6',
                 'train-1',
                 'train-11',
                 'train-20',
                 'train-7',
                 'truck-16',
                 'truck-3',
                 'truck-6',
                 'truck-7',
                 'turtle-16',
                 'turtle-5',
                 'turtle-8',
                 'turtle-9',
                 'umbrella-17',
                 'umbrella-19',
                 'umbrella-2',
                 'umbrella-9',
                 'yoyo-15',
                 'yoyo-17',
                 'yoyo-19',
                 'yoyo-7',
                 'zebra-10',
                 'zebra-14',
                 'zebra-16',
                 'zebra-17',
                 'elephant-1',
                 'elephant-12',
                 'elephant-16',
                 'elephant-18',
                 'goldfish-3',
                 'goldfish-7',
                 'goldfish-8',
                 'goldfish-10',
                 'hat-1',
                 'hat-2',
                 'hat-5',
                 'hat-18',
                 'kite-4',
                 'kite-6',
                 'kite-10',
                 'kite-15',
                 'motorcycle-1',
                 'motorcycle-3',
                 'motorcycle-9',
                 'motorcycle-18',
                 'mouse-1',
                 'mouse-8',
                 'mouse-9',
                 'mouse-17',
                 'flag-3',
                 'flag-9',
                 'flag-5',
                 'flag-2',
                 'frog-3',
                 'frog-4',
                 'frog-20',
                 'frog-9',
                 'gametarget-1',
                 'gametarget-2',
                 'gametarget-7',
                 'gametarget-13',
                 'hand-2',
                 'hand-3',
                 'hand-9',
                 'hand-16',
                 'helmet-5',
                 'helmet-11',
                 'helmet-19',
                 'helmet-13',
                 'licenseplate-6',
                 'licenseplate-12',
                 'licenseplate-13',
                 'licenseplate-15',
                 'electricfan-1',
                 'electricfan-10',
                 'electricfan-18',
                 'electricfan-20',
                 'chameleon-3',
                 'chameleon-6',
                 'chameleon-11',
                 'chameleon-20',
                 'crocodile-3',
                 'crocodile-4',
                 'crocodile-10',
                 'crocodile-14',
                 'gecko-1',
                 'gecko-5',
                 'gecko-16',
                 'gecko-19',
                 'fox-2',
                 'fox-3',
                 'fox-5',
                 'fox-20',
                 'giraffe-2',
                 'giraffe-10',
                 'giraffe-13',
                 'giraffe-15',
                 'gorilla-4',
                 'gorilla-6',
                 'gorilla-9',
                 'gorilla-13',
                 'hippo-1',
                 'hippo-7',
                 'hippo-9',
                 'hippo-20',
                 'horse-1',
                 'horse-4',
                 'horse-12',
                 'horse-15',
                 'kangaroo-2',
                 'kangaroo-5',
                 'kangaroo-11',
                 'kangaroo-14',
                 'leopard-1',
                 'leopard-7',
                 'leopard-16',
                 'leopard-20',
                 'lion-1',
                 'lion-5',
                 'lion-12',
                 'lion-20',
                 'lizard-1',
                 'lizard-3',
                 'lizard-6',
                 'lizard-13',
                 'microphone-2',
                 'microphone-6',
                 'microphone-14',
                 'microphone-16',
                 'monkey-3',
                 'monkey-4',
                 'monkey-9',
                 'monkey-17',
                 'shark-2',
                 'shark-3',
                 'shark-5',
                 'shark-6',
                 'squirrel-8',
                 'squirrel-11',
                 'squirrel-13',
                 'squirrel-19',
                 'volleyball-1',
                 'volleyball-13',
                 'volleyball-18',
                 'volleyball-19']

input_ptah = '/home/lsw/LSW/projects/tools/other/input/lasot'
trackers = sorted(os.listdir(input_ptah))
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/other/output/lasot'
data_path = '/media/lsw/data/LaSOT/zip'

for j, m in enumerate(sequence_list):
    mean_iou = []
    for i, n in enumerate(trackers):
        bbox_file = os.path.join(bbox_path[i], '{}.txt'.format(m))
        bbox = np.loadtxt(bbox_file, delimiter='\t')

        anno_file = '{}/{}/{}/groundtruth.txt'.format(data_path, m.split('-')[0], m)
        anno = np.loadtxt(anno_file, delimiter=',')

        save_dir = '{}/{}'.format(save_path, m)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        ious = []
        for k in range(1, bbox.shape[0], 1):
            iou = box_iou_xywh(bbox[k], anno[k])
            ious.append(iou)
        mean_iou.append(np.array(ious).mean())

        with open(os.path.join(save_dir, '{}.txt'.format(n)), 'a') as f:
            f.write(str(ious)[1:-1])
            f.close()







