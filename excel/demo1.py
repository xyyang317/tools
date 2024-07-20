import json
import os

import numpy as np
import pandas as pd

def jsondata(file_name='', max=True):
    with open(file_name, 'r') as f:
        json_data = json.load(f)

    datasets = list(json_data.keys())
    epochs = list(json_data[datasets[0]].keys())
    data = {}

    avg_prec = []
    for e in epochs:
        if e == 'epoch2802':
            continue
        p = []
        for d in datasets:
            p.append(round(100 * json_data[d][e]['precision_score'], 1))
        avg_prec.append(np.mean(p))

    if max:
        epochs = [epochs[np.argmax(avg_prec)]]

    name = os.path.split(file_name)[1][:-5]
    temp = name.split('-')
    w = temp[0]
    bs = 32 if len(temp) == 1 else temp[1]
    weight = np.array([w] * len(epochs))
    batch_size = np.array([bs] * len(epochs))

    data.update({'weight': weight.tolist()})
    data.update({'batch_size': batch_size.tolist()})
    data.update({'epoch': [e[-4:-1] for e in epochs]})

    for d in datasets:
        prec = []
        succ = []
        for e in epochs:
            prec.append(round(100 * json_data[d][e]['precision_score'], 1))
            succ.append(round(100 * json_data[d][e]['success_score'], 1))

        data.update({'{}_p'.format(d): prec})
        data.update({'{}_s'.format(d): succ})

    return data


def toxls(data):
    item =  list(data[0].keys())
    save_data = {}
    for i in item:
        temp = []
        for d in data:
            temp += d[i]
        save_data.update({i: temp})

    save_path = '{}/outputs'.format(os.getcwd())
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    save_name = '{}/out3.xlsx'.format(save_path)
    df = pd.DataFrame(save_data)
    df.to_excel(save_name, index=False)


path = 'input'
data = []
files = os.listdir(path)
files.sort()
for i in files:
    file_name = os.path.join(path, i)
    d = jsondata(file_name=file_name)
    data.append(d)

toxls(data)
