import os

import numpy as np

input_ptah = '/home/lsw/LSW/projects/tools/iou/input'
save_path = '/home/lsw/LSW/projects/tools/iou/input/nat2024/tab'
data_list = ['nat2024']
for dataset in data_list:
    print(dataset)
    tracker_list = ['TCTrack', 'UDAT-BAN']
    for tracker in tracker_list:
        print('\t'+tracker)
        file_list = os.listdir(os.path.join(input_ptah, dataset, tracker))
        for file in file_list:
            data = np.loadtxt(os.path.join(input_ptah, dataset, tracker, file), delimiter=' ')
            savetxt_path = os.path.join(save_path, dataset, tracker)
            if not os.path.exists(savetxt_path):
                os.makedirs(savetxt_path)
            save_name = os.path.join(savetxt_path, file)
            np.savetxt(save_name, data, fmt='%d', delimiter='\t')