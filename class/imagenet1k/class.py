import json
import os
import sys

import cv2

import timm


import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import math
import cv2 as cv
import torch.nn.functional as F
import numpy as np
import cv2

from lib.test.evaluation.coco import MSCOCO
from lib.test.evaluation.got10kdataset import GOT10KDataset
from lib.test.evaluation.lasotdataset import LaSOTDataset
from lib.test.evaluation.trackingnetdataset import TrackingNetDataset


def sample_target(im, target_bb, search_area_factor,output_sz=None, mask=None,name=0):
    if not isinstance(target_bb, list):
        x, y, w, h = target_bb.tolist()
    else:
        x, y, w, h = target_bb
    # Crop image
    crop_sz = math.ceil(math.sqrt(w * h) * search_area_factor)

    if crop_sz < 1:
        print(name)
        raise Exception('Too small bounding box.')

    x1 = round(x + 0.5 * w - crop_sz * 0.5)
    x2 = x1 + crop_sz

    y1 = round(y + 0.5 * h - crop_sz * 0.5)
    y2 = y1 + crop_sz

    x1_pad = max(0, -x1)
    x2_pad = max(x2 - im.shape[1] + 1, 0)

    y1_pad = max(0, -y1)
    y2_pad = max(y2 - im.shape[0] + 1, 0)

    # Crop target
    im_crop = im[y1 + y1_pad:y2 - y2_pad, x1 + x1_pad:x2 - x2_pad, :]
    if mask is not None:
        mask_crop = mask[y1 + y1_pad:y2 - y2_pad, x1 + x1_pad:x2 - x2_pad]

    # Pad
    im_crop_padded = cv.copyMakeBorder(im_crop, y1_pad, y2_pad, x1_pad, x2_pad, cv.BORDER_CONSTANT)
    # deal with attention mask
    H, W, _ = im_crop_padded.shape
    att_mask = np.ones((H,W))
    end_x, end_y = -x2_pad, -y2_pad
    if y2_pad == 0:
        end_y = None
    if x2_pad == 0:
        end_x = None
    att_mask[y1_pad:end_y, x1_pad:end_x] = 0
    if mask is not None:
        mask_crop_padded = F.pad(mask_crop, pad=(x1_pad, x2_pad, y1_pad, y2_pad), mode='constant', value=0)

    if output_sz is not None:
        resize_factor = output_sz / crop_sz
        im_crop_padded = cv.resize(im_crop_padded, (output_sz, output_sz))
        att_mask = cv.resize(att_mask, (output_sz, output_sz)).astype(np.bool_)
        if mask is None:
            return im_crop_padded, resize_factor, att_mask
        mask_crop_padded = \
        F.interpolate(mask_crop_padded[None, None], (output_sz, output_sz), mode='bilinear', align_corners=False)[0, 0]
        return im_crop_padded, resize_factor, att_mask, mask_crop_padded

    else:
        if mask is None:
            return im_crop_padded, att_mask.astype(np.bool_), 1.0
        return im_crop_padded, 1.0, att_mask.astype(np.bool_), mask_crop_padded

if __name__=="__main__":
    model = timm.create_model('mobilenetv3_large_100', pretrained=True)
    model.eval()
    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)


    dataset = GOT10KDataset()
    seq_list = dataset.get_sequence_list()

    dataset_name = seq_list[0].dataset
    report_file = '/home/lsw/LSW/projects/class/{}.json'.format(dataset_name)
    if not os.path.isfile(report_file):
        file = open(report_file, 'w')
        file.write('{}')
        file.close()

    with open(report_file, 'r', encoding='utf8') as fp:
        class_list = json.load(fp)

    for i in range(len(seq_list)):
        image = cv2.imread(seq_list[i].frames[0])
        target_bb = seq_list[i].ground_truth_rect[1]
        name = seq_list[i].name
        search_area_factor = 1.5
        output_sz = 224
        im, _, _ = sample_target(image, target_bb, search_area_factor, output_sz, name=name)
        im = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        tensor = transform(im).unsqueeze(0)

        import torch
        with torch.no_grad():
            out = model(tensor)
        probabilities = torch.nn.functional.softmax(out[0], dim=0)

        with open("/home/lsw/LSW/other/pytorch-image-models-main/imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]

        # Print top categories per image
        top1_prob, top1_catid = torch.topk(probabilities, 1)
        # print(top1_catid.item(), categories[top1_catid[0]], top1_prob[0].item())
        class_list.update({name:categories[top1_catid[0]]})

        print("\r", end="")
        print("progress : \033[1;31m{:.1f}% \033[0m [".format(round(100 * (i + 1) / len(seq_list), 1)),
              "\033[1;32m|" * ((i + 1) // int(len(seq_list) / 100)),
              " " * (100 - ((i + 1) // int(len(seq_list) / 100))), end="\033[0m]")
        sys.stdout.flush()

    with open(report_file, 'w') as f:
        json.dump(class_list, f, indent=4)