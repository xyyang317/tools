import glob
import os

import cv2
import numpy as np
from tqdm import tqdm

sequence_list = ['DJI_0032']
input_ptah = '/home/lsw/LSW/projects/tools/visual/real_world/txt'
save_path = '/home/lsw/LSW/projects/tools/visual/real_world/bbox'
data_path = '/home/lsw/LSW/projects/tools/visual/real_world/frames'
color = (0, 0, 255)


for j, m in enumerate(sequence_list):
    bbox_path = os.path.join(input_ptah,'{}.txt'.format(m))
    bbox = np.loadtxt(bbox_path, delimiter='\t').astype('int_')

    image_path = '{}/{}/img'.format(data_path, m)
    images = sorted(glob.glob(os.path.join(image_path, '*.jpg')))

    save_dir = '{}/{}'.format(save_path, m)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    pbar = tqdm(total=int(len(images)))
    for i, im in enumerate(images):
        image = cv2.imread(im)
        GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        x1, y1, w1, h1 = bbox[i]
        draw = cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), color, 2)

        cv2.imwrite(os.path.join(save_dir, "{}.jpg".format(i)), draw)
        pbar.update(1)
