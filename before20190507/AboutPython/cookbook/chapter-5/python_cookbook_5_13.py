# 获取文件夹中的文件列表

import os
names=os.listdir('/Users/purplecity')
print(names)

names=[ name for name in os.listdir('/Users/purplecity') if os.path.isfile(os.path.join('/Users/purplecity',name))]
print(names)

dirnames=[ name for name in os.listdir('/Users/purplecity') if os.path.isdir(os.path.join('/Users/purplecity',name))]
print(dirnames)

pyfiles=[ name for name in os.listdir('/Users/purplecity') if name.endswith('.py')]
print(pyfiles)

#文件名匹配，glob或者fnmatch模块

import glob
pyfiles=glob.glob('/Users/purplecity/*.py')

from fnmatch import fnmatch
fnmatch_pyfiles=[ name for name in os.listdir('/Users/purplecity') if fnmatch(name,'*.py') ]



