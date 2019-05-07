# 读取嵌套和可变长二进制数据  这些数据可能包含图片、视频、电子地图文件等。

polys = [
    [ (1.0, 2.5), (3.5, 4.0), (2.5, 1.5) ],
    [ (7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0) ],
    [ (3.4, 6.3), (1.2, 0.5), (4.6, 9.2) ],
]

# print(len(polys)) #3

# 搓比代码

import struct,itertools

#print(list(itertools.chain(*polys)))
#[(1.0, 2.5), (3.5, 4.0), (2.5, 1.5), (7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0), (3.4, 6.3), (1.2, 0.5), (4.6, 9.2)]

def write_polys(filename,polys):
  flattened=list(itertools.chain(*polys))
  min_x=min(x for x,y in flattened)
  max_x=max(x for x,y in flattened)
  min_y=min(y for x,y in flattened)
  max_y=max(y for x,y in flattened)

  with open(filename,'wb') as f:
      f.write(struct.pack('<idddddi',0x1234,min_x,min_y,max_x,max_y,len(polys)))
      #把头部写进去

      for poly in polys:
          size=len(poly) * struct.calcsize('dd')
          # struct.calcsize用于计算格式字符串所对应的结果的长度，如：struct.calcsize('ii')，返回8。因为两个int类型所占用的长度是8个字节。
          #polys每个元素是列表，len后是元组的个数，每个元组两个dd字节
          f.write(struct.pack('<i',size+4))  #4是指记录长度的字节
          #记录长度
          for pt in poly:
              f.write(struct.pack('<dd',*pt))
              #每个元组写进去

def read_polys(filename):
    with open(filename,'rb') as f:
        header=f.read(40)
        #读头

        file_code,min_x,min_y,max_x,max_y,num_polys=struct.unpack('<iddddi',header)
        polys=[]
        for n in range(num_polys):
            pbytes, = struct.unpack('<i',f.read(4))
            #先解压坐标值的长度
            poly=[]
            for m in range(pbytes):
                pt = struct.unpack('<dd',f.read(16))
                poly.append(pt)
            polys.append(poly)
    return polys

# 666


# 高级方法，全书最高级最复杂的方法。大量使用面向对象编程和

# 当读取字节数据的时候，通常在文件开始部分会包含文件头和其他的数据结构。 尽管struct模块可以解包这些数据到一个元组中去，另外一种表示这种信息的方式就是使用一个类

class  StructField:
    def __init__(self,format,offset):
        self.format=format
        self.offset=offset

    def __get__(self,instance,cls):
        if instance is None:
            return self

        else:
            r = struct.unpack_from(self.format,instance._buffer,self.offset)
            return r[0] if len(r) == 1 else r

class Structure:
    def __init__(self,bytedata):
        self._buffer=memoryview(bytedata)


# 显然Structure救生衣被StructField使用的
# Structure 类就是一个基础类，接受字节数据并存储在内部的内存缓冲中
# struct.unpack_from() 函数被用来从缓冲中解包一个值，省去了额外的分片或复制操作步骤。
# 这里直接upack_from当做函数使用了。本来是s=Struct(format) s.unpack_from(data,offset)操作的



class PolyHeader(Structure):
    file_code=StructField('<i',0)
    min_x=StructField('<d',4)
    min_y=StructField('<d',12)
    max_x=StructField('<d',20)
    max_y=StructField('<d',28)
    num_polys=StructField('<i',36)

f=open('polys.bin','rb')
phead=PolyHeader(f.read(40))