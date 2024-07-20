import os

from cv2 import VideoCapture
from cv2 import imwrite
from tqdm import tqdm
import cv2

def save_image(image, addr, num):
    address = '{}{:05d}.jpg'.format(addr, num)
    imwrite(address, image)


if __name__ == '__main__':

    video_path = "./videos/DJI_0031.MOV"  # 视频路径
    out_path = "./frames/" + os.path.split(video_path)[1][:-4] + '/img/'  # 保存图片路径+名字
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    is_all_frame = True  # 是否取所有的帧
    time_interval = 1  # 时间间隔

    # 读取视频文件
    videoCapture = VideoCapture(video_path)

    # 读帧
    success, frame = videoCapture.read()

    i = 0
    j = 0

    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    pbar = tqdm(total=int(frames/time_interval))
    while success:
        i = i + 1
        if (i % time_interval == 0):
            j = j + 1
            save_image(frame, out_path, j)
            pbar.update(1)

        success, frame = videoCapture.read()

