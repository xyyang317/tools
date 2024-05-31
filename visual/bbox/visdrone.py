import glob
import os

import cv2
import numpy as np


sequence_list = ['uav0000074_01656_s']
input_ptah = '/home/lsw/LSW/projects/tools/visual/bbox/input/visdrone'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['HiFT', 'TCTrack', 'HiT', 'MixFormerV2', 'AutoTrack', 'ARCH-HC', 'F-SiamFC++', 'P-SiamFC++', 'TATrack']
bbox_path1 = [os.path.join(input_ptah, t) for t in ['HiFT', 'TCTrack']]
bbox_path2 = [os.path.join(input_ptah, t) for t in ['HiT', 'MixFormerV2', 'AutoTrack', 'ARCH-HC',  'F-SiamFC++', 'P-SiamFC++', 'TATrack']]
color = [(255, 255, 0), (254, 38, 34), (68, 255, 255), (0, 255, 0), (0, 0, 0), (219, 0, 219), (189, 114, 0), (142, 47, 126), (0, 0, 255)]
save_path = '/home/lsw/LSW/projects/tools/visual/bbox/output/visdrone'
data_path = '/home/lsw/data/VisDrone2018'


for j, m in enumerate(sequence_list):
    bbox_file1 = [os.path.join(bp, '{}.txt'.format(m)) for bp in bbox_path1]
    bbox1 = [np.loadtxt(bf, delimiter=',').astype('int_') for bf in bbox_file1]
    bbox_file2 = [os.path.join(bp, '{}.txt'.format(m)) for bp in bbox_path2]
    bbox2 = [np.loadtxt(bf, delimiter='\t').astype('int_') for bf in bbox_file2]
    bbox = bbox1 + bbox2

    anno_file = '{}/annotations/{}.txt'.format(data_path, m)
    anno = np.loadtxt(anno_file, delimiter=',').astype('int_')

    image_path = '{}/sequences/{}'.format(data_path, m)
    images = sorted(glob.glob(os.path.join(image_path, '*.jpg')))

    save_dir = '{}/{}'.format(save_path, m)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    for i, im in enumerate(images):
        image = cv2.imread(im)
        GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        x, y, w, h = anno[i]

        for k, t in enumerate(trackers):
            x1, y1, w1, h1 = bbox[k][i]
            draw = cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), color[k], 5)
            # draw = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5) #gt

        cv2.imwrite(os.path.join(save_dir, "{}.jpg".format(i)), draw)


