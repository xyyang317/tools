import glob
import os

import cv2
import numpy as np


sequence_list = ['L07001','L05011','L05005','L05015','L03001','L05017','L02001','L06002','L05016','L09002']
input_ptah = '/home/lsw/LSW/projects/tools/iou/input/nat2024'
# trackers = sorted(os.listdir(input_ptah))
trackers = ['UDAT-BAN', 'Sam-DA', 'DCPT', 'TCTrack', 'Aba-ViTrack', 'AVTrack', 'MambaNUT']
bbox_path = [os.path.join(input_ptah, t) for t in trackers]
save_path = '/home/lsw/LSW/projects/tools/visual/bbox/output/nat2024'
data_path = '/home/lsw/data/NAT2024-1'
colors = [ (68, 255, 255), (0,140,255), (219, 0, 219), (189, 114, 0), (255,0,107), (128,100,234), (0, 0, 255)]

for j, m in enumerate(sequence_list):
    bbox_file1 = [os.path.join(bp, '{}.txt'.format(m)) for bp in bbox_path]
    bbox = [np.loadtxt(bf, delimiter='\t').astype('int_') for bf in bbox_file1]

    anno_file = '{}/anno/{}.txt'.format(data_path, m)
    anno = np.loadtxt(anno_file, delimiter=',').astype('int_')

    image_path = '{}/data_seq/{}'.format(data_path, m)
    images = sorted(glob.glob(os.path.join(image_path, '*.jpg')))

    save_dir = '{}/{}'.format(save_path, m)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    for i, im in enumerate(images):
        image = cv2.imread(im)
        GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        x, y, w, h = anno[i]

        draw = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # gt
        for k, t in enumerate(trackers):
            x1, y1, w1, h1 = bbox[k][i]
            draw = cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), colors[k], 2)

        cv2.imwrite(os.path.join(save_dir, "{}.jpg".format(i)), draw)


# width, height = 200, 400
# blank_image = np.ones((height, width, 3), dtype=np.uint8) * 255
# font = cv2.FONT_HERSHEY_SIMPLEX
# font_scale = 0.75
# thickness = 2
# text_x = 10  # 文本的x坐标（左边距）
# text_y = 50  # 文本的起始y坐标
# for i, tracker in enumerate(trackers):
#     text_position = (text_x, text_y + i * 40)
#     cv2.putText(blank_image, tracker, text_position, font, font_scale, colors[i], thickness, cv2.LINE_AA)
# cv2.imwrite(os.path.join(save_path, 'trackers.png'), blank_image)
#
#
