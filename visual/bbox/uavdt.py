import glob
import os

import cv2
import numpy as np


sequence_list = ['S1501']
input_ptah = '/home/lsw/LSW/projects/tools/visual/bbox/input/uavdt'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['AutoTrack', 'SiamAPN', 'HiFT', 'TCTrack', 'AVTrack', 'Aba-ViTrack', 'Aba-ViTrack++']
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/visual/bbox/output/uavdt'
data_path = '/home/lsw/data/UAVDT'
color = [ (68, 255, 255), (0,140,255), (219, 0, 219), (189, 114, 0), (0,0,0), (34,139,34), (0, 0, 255)]



for j, m in enumerate(sequence_list):
    bbox_file1 = [os.path.join(bp, '{}.txt'.format(m)) for bp in bbox_path]
    bbox = [np.loadtxt(bf, delimiter='\t').astype('int_') for bf in bbox_file1]

    anno_file = '{}/anno/{}_gt.txt'.format(data_path, m)
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
            draw = cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), color[k], 2)
            # draw = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5) #gt

        cv2.imwrite(os.path.join(save_dir, "{}.jpg".format(i)), draw)


