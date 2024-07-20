import os
from pathlib import Path

path = '/home/lsw/LSW/projects/tools/visual/real_world/bbox/DJI_0032'
list = os.listdir(path)
list.sort()
for i in list:
    oldname = os.path.join(path,i)
    newname = os.path.join(path, '{:05d}.jpg'.format(int(i[:-4])-int(list[0][:-4])+1))
    os.rename(oldname,newname)