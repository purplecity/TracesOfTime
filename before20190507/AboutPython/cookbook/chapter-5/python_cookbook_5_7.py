# 读写压缩文件

#gzip bz2模块可以处理对应的压缩文件

import gzip,bz2

with gzip.open('somefile.gz','rt') as f:
    text=f.read()

with bz2.open('somefile.gz2','rt') as f:
    text2=f.read()


with gzip.open('somefile.gz','wt') as f:
    f.write(text)

with bz2.open('somefile.bz2','wt') as f:
    f.write(text2)


#如果你不指定模式，那么默认的就是二进制模式，如果这时候程序想要接受的是文本数据，那么就会出错。 gzip.open() 和 bz2.open() 接受跟内置的 open() 函数一样的参数， 包括 encoding，errors，newline 等等。

