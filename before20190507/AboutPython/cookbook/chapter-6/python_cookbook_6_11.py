# 读写二进制数组数据

#读写一个二进制数组的结构化数据到Python元组中。

'''
python 只定义了六种基本类型：字符串，整数，浮点数，元组，列表，字典
当Python需要通过网络与其他的平台进行交互的时候，必须考虑到将这些数据类型与其他平台或语言之间的类型进行互相转换问题
C++写的客户端发送一个int型(4字节)变量的数据到Python写的服务器，Python接收到表示这个整数的4个字节数据，怎么解析成Python认识的整数呢？
Python的标准模块struct就用来解决这个问题。

C语言中常用类型与Python类型对应的格式符
在Format string 的首位，有一个可选字符来决定大端和小端  对应到python是integer，float，float

'<idd' 小端 int double double

'''
# 将一个Python元组列表写入一个二进制文件，并使用 struct 将每个元组编码为一个结构体(不是c语言的结构体)

from struct import Struct
def write_records(records,format,f):
    record_struct=Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))

'''
struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，
可以把这里的字符串理解为字节流，或字节数组）
'''

records = [ (1, 2.3, 4.5),
            (6, 7.8, 9.0),
            (12, 13.4, 56.7) ]
with open('data.b','wb') as f:
    write_records(records,'<idd',f)



# 读取这个文件并返回一个元组列表
## 以块的形式增量读取文件

def read_records(format,f):
    record_struct=Struct(format)
    chunks=iter(lambda: f.read(record_struct.size),b'')
    return (record_struct.unpack(chunks) for chunk in chunks)


with open('data.b','rb') as f:
    for rec in read_records('<idd',f):
        ...

# 有点意犹未尽，迭代器与for结合。 返回一个生成器，再与for结合


#将整个文件一次性读取到一个字节字符串中，然后在分片解析

def unpack_records(format,data):
    record_struct=Struct(format)
    return (record_struct.unpack_from(data,offset) for offset in range(0,len(data),record_struct.size))




with open('data.b','rb') as f:
    data=f.read()
for rec in unpack_records('<idd',data):
    ...

#  意猶未盡。第一种方法是读几次，然后相应的解压几次，第二种方法是，读整个。然后解压几次.一个是unpack一个是unpackform



'''
对于需要编码和解码二进制数据的程序而言，通常会使用 struct 模块。 为了声明一个新的结构体，只需要像这样创建一个 Struct 实例
'''

record_struct=Struct('<idd')
print(record_struct.size)
print(record_struct.pack(1,2.0,3.0))  #b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@'
print(record_struct.unpack(_))  #(1, 2.0, 3.0)

# 不建议struct.pack('<idd', 1, 2.0, 3.0)  struct.unpack('<idd', _)这种方法操作

'''

unpack_from() 对于从一个大型二进制数组中提取二进制数据非常有用， 因为它不会产生任何的临时对象或者进行内存复制操作。
 你只需要给它一个字节字符串(或数组)和一个字节偏移量，它会从那个位置开始直接解包数据。
'''

#通过元组来创建一个nametuple的实例
from collections import namedtuple

Recordhhe= namedtuple('Record',['kind','x','y'])
with open('data,p','rb') as f:
    recordhhe=(Recordhhe(*r) for r in read_records('<idd',f))

for r in recordhhe:
    print(r.kind,r.x,r.y)
'''
User = namedtuple('User', ['name', 'sex', 'age'])

# 创建一个User对象
user = User(name='kongxx', sex='male', age=21)
'''


# 之前的读是把二进制数据读到一个元组列表中
#如果要处理大量的数据的话，最好是用numpy模块，放到一个结构化数组中

import numpy as np

f=open('data.b','rb')
recordx=np.fromfile(f,dtype='<i,<d,<d')
print(recordx)
'''
array([(1, 2.3, 4.5), (6, 7.8, 9.0), (12, 13.4, 56.7)],
dtype=[('f0', '<i4'), ('f1', '<f8'), ('f2', '<f8')])
'''
print(recordx[0],recordx[1])
# (1, 2.3, 4.5),(6, 7.8, 9.0)


#作者总结  先检查看看Python是不是已经提供了现存的模块。因为不到万不得已没有必要去重复造轮子。