# 跳过可迭代对象的开始部分
# 比如文件的注释  本节的方案适用于所有可迭代对象，包括那些事先不能确定大小的， 比如生成器，文件及其类似的对象。



from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'),f):
        print(line,end='')


#比较区别
with open('/etc/passwd') as f:
    lines=(line for line in f if not line.startswith('#'))
    for line in lines:
        print(line,end='')
#这里是去掉所有#开头的注释。上一个值只跳过开头的注释


#如果知道了要跳过元素的个数

from itertools import islice
items=['a','b', 'c', 1, 4, 10, 15]
for x in islice(items,3,None): #start  stop   类似于[3:] [:3]
    print(x)

