import glob
import os

import cv2
import numpy as np


sequence_list = ['train-11']
input_ptah = '/home/lsw/LSW/projects/tools/visual/bbox/input/lasot'
trackers = sorted(os.listdir(input_ptah))
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/visual/bbox/output/lasot'
data_path = '/media/lsw/data/LaSOT/zip'

for j, m in enumerate(sequence_list):
    bbox_file = [os.path.join(bp, '{}.txt'.format(m)) for bp in bbox_path]
    bbox = [np.loadtxt(bf, delimiter='\t').astype('int_') for bf in bbox_file]

    anno_file = '{}/{}/{}/groundtruth.txt'.format(data_path, m.split('-')[0], m)
    anno = np.loadtxt(anno_file, delimiter=',').astype('int_')

    image_path = '{}/{}/{}/img'.format(data_path, m.split('-')[0], m)
    images = sorted(glob.glob(os.path.join(image_path, '*.jpg')))

    save_dir = '{}/{}'.format(save_path, m)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    for i, im in enumerate(images):
        image = cv2.imread(im)
        GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        x, y, w, h = anno[i]
        x1, y1, w1, h1 = bbox[0][i]
        x2, y2, w2, h2 = bbox[1][i]

        draw_1 = cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), (180 ,119, 31), 5)
        draw_2 = cv2.rectangle(image, (x2, y2), (x2 + w2, y2 + h2), (14, 127, 255), 5)
        draw = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
        cv2.imwrite(os.path.join(save_dir, "{}.jpg".format(i)), draw_2)


