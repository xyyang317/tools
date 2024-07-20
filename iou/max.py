import os

import numpy as np

input_ptah = '/home/lsw/LSW/projects/tools/other/bear-4'
trackers = sorted(os.listdir(input_ptah))
length = np.loadtxt(os.path.join(input_ptah, trackers[0]), delimiter=',').shape[0]

ious = [np.loadtxt(os.path.join(input_ptah, t), delimiter=',') for t in trackers]

max = []
for i in range(length):
    iou = np.array([ious[t][i] for t,_ in enumerate(trackers)])
    max.append(np.argmax(iou))
print(max)