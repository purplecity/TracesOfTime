# 创建数据处理管道.看了一个小时。真是意犹未尽

#数据管道(类似Unix管道)的方式迭代处理数据。 比如，你有个大量的数据需要处理，但是不能将它们一次性放入内存中。


#关键理解  重点是要明白 yield 语句作为数据的生产者而 for 循环语句作为数据的消费者。每一个生成器函数中都有for语句！！！！ 当这些生成器被连在
# 一起后，每个 yield 会将一个单独的数据元素传递给迭代处理管道的下一阶段。还真是管道模型！

import os,fnmatch,gzip,bz2,re

def gen_find(filepat,top):
    for path,dirlist,filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield  os.path.join(path,name)


#找到top目录下所有符合filepat匹配模式的文件的文件路径
#os.walk() 方法用于通过在目录树中游走输出在目录中的文件名，向上或者向下。
# os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])
'''
top -- 是你所要遍历的目录的地址, 返回的是一个三元组(root,dirs,files)。
root 所指的是当前正在遍历的这个文件夹的本身的地址
dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
'''


def gen_opener(filenames):
    for filename in filenames:
        if filename.endswith('.gz'):
            f=gzip.open(filename,'rt')
        elif filename.endswith('.bz2'):
            f=bz2.open(filename,'rt')
        else:
            f=open(filename,'rt')
        yield f
        f.close()

# gen_opener() 生成器每次生成一个打开过的文件， 等到下一个迭代步骤时文件就关闭了

def gen_concatenate(iterators):
    for it in iterators:
        yield  from it   #yield from it 简单的返回生成器 it 所产生的所有值

def gen_grep(pattern,lines):
    pat=re.compile(pattern)
    for line in lines:
        if  pat.search(line):
            yield line

'''
日志目录：
foo/
    access-log-012007.gz
    access-log-022007.gz
    access-log-032007.gz
    ...
    access-log-012008
bar/
    access-log-092007.bz2
    ...
    access-log-022008
    
每个日志文件：
124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -


'''


lognames=gen_find('access-log*','www')
files=gen_opener(lognames)
lines=gen_concatenate(files)   #所有access-log*文件的所有行数
pylines=gen_grep('(?i)python',lines)
for line in pylines:
    print(line)

'''
*是解压的意思，看来不止可以解压list。还可以解压生成器函数，生成器。这里*files确实是每个文件所有行的总集合
形式为([file1_line1,file1_lin2...],[file2_line2,file2_line2...]...)
导致被提前消费掉的意思是，itertools.chain() 接受一个或多个可迭代对象作为输入参数。 然后创建一个迭代器，依次连续
的返回每个可迭代对象中的元素。依次迭代get_opener的话确实全部消耗掉了。而且，没yield就close

这里是concatenate迭代的时候，一个一个迭代。刚好open的f也一个一个全部close的。
如果把close去掉，是可以的。只不过是一回全部生成文件对象f。而不是一个个的生成f然后close。这完全就是优秀程序员考虑的性能问题。我们理解就好了-。=
'''

files=gen_opener(lognames)
lines=gen_concatenate(files)   #所有access-log*文件的所有行数
pylines=gen_grep('(?i)python',lines)
bytecolumn=(line.rsplit(None,1)[1] for line in pylines)  #逆序分隔，分隔一次，分隔符是空格。取第一例。也就是取逆序到第一个空格的字符串
bytes=(int(x) for x in bytecolumn if x != '-')  # 以上面注释中每个日志文件,最后的数字来举例子的，这个日志格式很熟悉，很类似于nginx的日志
print('Total',sum(bytes))



'''
Python rsplit() 方法通过指定分隔符对字符串进行分割并返回一个列表，默认分隔符为所有空字符，包括空格、换行(\n)、制表符(\t)等。类似于 split() 方法，只不过是从字符串最后面开始分割。
rsplit() 方法语法：


S.rsplit([sep=None][,count=S.count(sep)])
回到顶部
参数

sep -- 可选参数，指定的分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
count -- 可选参数，分割次数，默认为分隔符在字符串中出现的总次数。


 
S = "this is string example....wow!!!"
print (S.rsplit( ))
print (S.rsplit('i',1))
print (S.rsplit('w'))
以上实例输出结果如下：


['this', 'is', 'string', 'example....wow!!!']
['this is str', 'ng example....wow!!!']
['this is string example....', 'o', '!!!']

'''
