# str与bytes的互相转换

#Python 3版本中，字符串是以Unicode编码所以有：
print('字符编码问题真令人touda!')

#对于单个字符的编码，Python提供了ord()函数获取字符的整数表示，chr()函数把编码转换为对应的字符：
print(ord('A'),ord('中'),chr(66),chr(25991))


#Python的字符串类型是str，在内存中以Unicode表示，一个字符对应若干个字节。如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes
x=b'ABC' #bytes
y='ABC'  #str

print('ABC'.encode('ascii'),'中文'.encode('utf-8'))  #str->bytes
print(b'ABC'.decode('ascii'),b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))  #bytes->str

#len()函数计算的是str的字符数，如果换成bytes，len()函数就计算字节数
print(len(b'ABC'),len(b'\xe4\xb8\xad\xe6\x96\x87'),len('中文'.encode('utf-8')),len('ABC'))


#至于字符串到整数的转换就算了。ip整数字符串转化有相应的方法。不纠结。