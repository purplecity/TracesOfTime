# 测试文件存不存在

import os


path='/etc/passwd'

print(os.path.exists(path))
print(os.path.isfile(path))
print(os.path.isdir(path))
print(os.path.islink('/usr/bin/python'))
print(os.path.realpath('/usr/bin/python'))

print(os.path.getsize(path))
print(os.path.getmtime(path))

import time
print(time.ctime(os.path.getmtime(path)))