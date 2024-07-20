import scipy.io as sio
import numpy as np
import os

from tqdm import tqdm

# 先读取单个mat文件来看看mat文件的长什么样
# matdata = sio.loadmat("/home/lsw/LSW/projects/tools/mat2txt/input/dtb70/AutoTrack/Animal1_AutoTrack.mat")
# data = matdata['results'][0][0][0][0][1]
# 下面是正式开始批量处理啦
# 读取存放批量.mat的文件夹中的所有.mat文件的文件名

input_ptah = '/home/lsw/LSW/projects/tools/mat2txt/input'
save_path = '/home/lsw/LSW/projects/tools/mat2txt/output'
data_list = os.listdir(input_ptah)
for dataset in data_list:
    print(dataset)
    tracker_list = os.listdir(os.path.join(input_ptah, dataset))
    for tracker in tracker_list:
        print('\t'+tracker)
        mat_list = os.listdir(os.path.join(input_ptah, dataset, tracker))
        for mat in mat_list:
            matdata = sio.loadmat(os.path.join(input_ptah, dataset, tracker, mat))
            data = matdata['results'][0][0][0][0][1]
            txt_filename = mat.split('_')[0] + ".txt"  # 例如将“0001.mat” 改为 “0001.txt”
            savetxt_path = os.path.join(save_path, dataset, tracker)
            if not os.path.exists(savetxt_path):
                os.makedirs(savetxt_path)
            save_name = os.path.join(savetxt_path, txt_filename)
            np.savetxt(save_name, data, fmt='%d', delimiter='\t')   # fmt为保存格式，可不填，会以默认格式保存
