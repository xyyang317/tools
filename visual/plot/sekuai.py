import numpy as np
import matplotlib.pyplot as plt

name = 'train-1'
x_file = '/home/lsw/LSW/projects/tools/visual/plot/input/blocks-our-{}.txt'.format(name)
# y_file = '/home/lsw/LSW/projects/tools/visual/plot/input/blocks-rand-{}.txt'.format(name)
x = []
with open(x_file) as f:
    line = f.readline()
    while line:
        a = line.split('[')[1].split(']')[0]
        b = [int(i) for i in a.split(', ')]
        x.append(b)
        line = f.readline()
f.close()

y = []
# with open(y_file) as f:
#     line = f.readline()
#     while line:
#         a = line.split('[')[1].split(']')[0]
#         b = [int(i) for i in a.split(', ')]
#         y.append(b)
#         line = f.readline()
# f.close()

for i, _ in enumerate(x):
    X= np.expand_dims(np.array(x[i]), axis=0)

    plt.figure(figsize=(10,1))
    plt.imshow(X,cmap='hot')
    plt.savefig('/home/lsw/LSW/projects/tools/visual/plot/output/sekuai/{}/our_{}.png'.format(name, i))
    plt.close()


    # Y= np.expand_dims(np.array(y[i]), axis=0)
    #
    # plt.figure(figsize=(10,1))
    # plt.imshow(Y,cmap='Blues')
    # plt.savefig('/home/lsw/LSW/projects/tools/visual/plot/output/sekuai/{}/rand_{}.png'.format(name, i))
    # plt.close()
