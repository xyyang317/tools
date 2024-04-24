file = '1'

xyz = []
with open(file) as f:
    line = f.readline()
    while line:
        a = line.split('(')[1].split(')')[0]
        b = tuple([int(i) for i in a.split(', ')])
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
            tmp += [j_idx+1]
            exist += [j_idx]
    if len(tmp) != 1:
        same.append(tmp)

for s in same:
    str = [xyz[i-1] for i in s]
    print('{}:{}'.format(s, str))