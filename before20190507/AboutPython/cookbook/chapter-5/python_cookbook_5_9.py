#  你想直接读取二进制数据到一个可变缓冲区中，而不需要做任何的中间复制操作。 或者你想原地修改数据并将它写回到一个文件中去。

# 就是之前的readinto方法,实际读取的字节数。


import os.path

def read_into_buffer(fileaname):
    buf=bytearray(os.path.getsize(fileaname))
    with open(fileaname,'rb') as f:
        f.readinto(buf)
    return buf


with open('sample.bin','wb') as f:
    f.write(b'helloworld')

buf=read_into_buffer('sample.bin')
buf[0:5]=b'letse'
with open('newsample.bin','wb') as f:
    f.write(buf)

# array bytearray

'''

Python bytearray() 函数
Python 内置函数 Python 内置函数
描述
bytearray() 方法返回一个新字节数组。这个数组里的元素是可变的，并且每个元素的值范围: 0 <= x < 256。
语法
bytearray()方法语法：
class bytearray([source[, encoding[, errors]]])
参数
如果 source 为整数，则返回一个长度为 source 的初始化数组；
如果 source 为字符串，则按照指定的 encoding 将字符串转换为字节序列；
如果 source 为可迭代类型，则元素必须为[0 ,255] 中的整数；
如果 source 为与 buffer 接口一致的对象，则此对象也可以被用于初始化 bytearray。
如果没有输入任何参数，默认就是初始化数组为0个元素。
'''

'''
文件对象的 readinto() 方法能被用来为预先分配内存的数组
填充数据，甚至包括由 array 模块或 numpy 库创建的数组。 
和普通 read() 方法不同的是， readinto() 填充已存在的缓冲
区而不是为新对象重新分配内存再返回它们。 因此，你可以使
用它来避免大量的内存分配操作。 比如，如果你读取一个由相同大
小的记录组成的二进制文件时，你可以像下面这样写：
'''

record_size=32
buf=bytearray(record_size)
with open('somefile', 'rb') as f:
    while True:
        n=f.readinto(buf)
        if n<record_size:
            break
        # Use the contents of buf
        ...


# memoryview  通过零复制的方式对已存在的缓冲区执行切片操作，甚至还能修改它的内容

buf=bytearray(b'Helloworld')
m1=memoryview(buf)
m2=m1[-5:]
m2[:]=b'WORLD'
print(buf)   #bytearray(b'Hello WORLD')
