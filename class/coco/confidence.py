import json

dataset_name = 'lasot'
report_file = '/home/lsw/LSW/projects/class/coco/{}.json'.format(dataset_name)
with open(report_file, 'r', encoding='utf8') as fp:
    class_list = json.load(fp)

split_file = '/home/lsw/LSW/projects/class/coco/{}_train_split.txt'.format(dataset_name)
for i in class_list:
    if dataset_name == 'lasot':
        if class_list[i]['class'] != i.split('-')[0]:
            continue
    if class_list[i]['score'] > 0.9:
        with open(split_file,'a') as f:
            if dataset_name == 'got10k':
                f.write(str(int(i[-6:])-1)+'\n')
            else:
                f.write(i + '\n')
            f.close()
