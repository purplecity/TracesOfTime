# 读写二进制文件如图片声音文件等
# rt read text rb read byte

with open('/Users/purplecity/a.txt','rb') as f:
    data=f.read()

with open('/Users/purplecity/a.txt','wb') as f:
    f.write(b'helloworld')


#在读取二进制数据时，需要指明的是所有返回的数据都是字节字符串格式的，而不是文本字符串。 类似的，在写入的时候，必须保证参数是以字节形式对外暴露数据的对象(比如字节字符串，字节数组对象等)。

# 索引和迭代动作返回的是字节的值而不是字节字符串

t='helloworld'
print(t[0])

for c in t:
    print(c)

b=b'helloworld'
print(b[0])

for x in b:
    print(x)

#想从二进制模式的文件中读取或写入文本数据，必须确保要进行解码和编码操作
with open('/Users/purplecity/a.txt','rb') as f:
    data=f.read(16)
    text=data.decode('utf-8')

with open('/Users/purplecity/a.txt','wb') as f:
    text='helloworld'
    f.write(text.encode('utf-8'))


import array
# 二进制I/O还有一个鲜为人知的特性就是数组和C结构体类型能直接被写入，而不需要中间转换为自己对象
a=array.array('i',[1,2,3])
with open('/Users/purplecity/a.txt','wb') as f:
    f.write(a)


# 很多对象还允许通过使用文件对象的 readinto() 方法直接读取二进制数据到其底层的内存中去。比如：
#这就是直接读取二进制数组对象到 变量中

b=array.array('i',[0,0,0,0,0])
with open('/Users/purplecity/a.txt','rb') as f:
    f.readinto(b)

print(b)

#array('i', [1, 2, 3, 0, 0])





