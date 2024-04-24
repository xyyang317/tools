file = '1'

xyz = []
with open(file) as f:
    line = f.readline()
    while line:
        a = line.split('(')[1].split(')')[0]
        b = [int(i) for i in a.split(', ')]
        xyz.append(b)
        line = f.readline()
f.close()

same = []
exist = []
for i_idx, i in enumerate(xyz):
    if i_idx in exist:
        continue
    tmp = [i_idx+1]
    for j_idx, j in enumerate(xyz):
        if i_idx == j_idx:
            continue
        elif i[0] == j[0] and i[1] == j[1]:
            if i[2] < j[2]-5:
                same.append([i_idx+1, j_idx+1])

for s in same:
    str = '{};{}'.format(xyz[s[0]-1], xyz[s[1]-1])
    print('{{{0}}};'.format(s))
    # print('{{{0}}};'.format(str))