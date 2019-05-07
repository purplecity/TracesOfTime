# 内存映射一个二进制文件到一个可变字节数组中，目的可能是为了随机访问它的内容或者是原地做些修改

#mmap
'''

需要强调的一点是，内存映射一个文件并不会导致整个文件被读取到内存
中。 也就是说，文件并没有被复制到内存缓存或数组中。相反，操作系统仅
仅为文件内容保留了一段虚拟内存。 当你访问文件的不同区域时，这些区域
的内容才根据需要被读取并映射到内存区域中。 而那些从没被访问到的部分
还是留在磁盘上。所有这些过程是透明的，在幕后完成！
'''


import os ,mmap

def memory_map(filename,access=mmap.ACCESS_WRITE):
    size=os.path.getsize(filename)
    fd=os.open(filename,os.O_RDWR)
    return mmap.mmap(fd,size,access=access)

#教你怎样初始创建一个文件并将其内容扩充到指定大小：
size=1000000
with open('data','wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

m=memory_map('data')

print(len(m),m[0:10])
m[0:11]=b'hello world'


#m.close()
with open('data','rb') as f:
    print(f.read(11))




#1000000 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# b'hello world'

#mmap()返回的mmap对象同样可以作为一个上下文管理器来使用，这时候底层的文件会被自动关闭。
# memort_map()函数打开的文件同时支持读写操作，任何修改内容都会复制原来的文件中。
#如果需要只读的访问模式，可以给参数 access 赋值为 mmap.ACCESS_READ 如果你想在本地修改数据，但是又不想将修改
# 写回到原始文件中，可以使用 mmap.ACCESS_COPY


# mmap() 所暴露的内存看上去就是一个二进制数组对象。 但是，你可以使用一个内存视图来解析其中的数据

'''

v=memoryview(m).cast('I')
print(v[0])

'''