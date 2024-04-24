import json
import os

import numpy as np
import pandas as pd


def json2xls(file_name='', max=True):
    with open(file_name, 'r') as f:
        json_data = json.load(f)

    datasets = list(json_data.keys())
    epochs = list(json_data[datasets[0]].keys())
    # epochs = ['epoch296']
    data = {}

    avg_prec = []
    for e in epochs:
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

    data.update({'weight': weight})
    data.update({'batch_size': batch_size})
    data.update({'epoch': e[-3:] for e in epochs})

    for d in datasets:
        prec = []
        succ = []
        for e in epochs:
            prec.append(round(100 * json_data[d][e]['precision_score'], 1))
            succ.append(round(100 * json_data[d][e]['success_score'], 1))

        data.update({'{}_p'.format(d): prec})
        data.update({'{}_s'.format(d): succ})

    save_path = '{}/outputs'.format(os.getcwd())
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    save_name = '{}/{}.xlsx'.format(save_path, name)
    df = pd.DataFrame(data)
    df.to_excel(save_name, index=False)


file_name = 'input/1-10.json'
json2xls(file_name=file_name)
