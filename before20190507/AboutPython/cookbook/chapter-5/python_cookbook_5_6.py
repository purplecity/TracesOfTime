# 字符串的io操作

#文件有read write print重定向到文件。字符串可以类似文件操作

import io
s=io.StringIO()
print(s.write('helloworld\n'))
print('this is a test',file=s)
print(s.getvalue())

x=io.StringIO('nice\neverybody\n')
print(x.read(3))
print(x.read())#是一点一点的读掉了字符串.....

#io.StringIO 只能用于文本。如果你要操作二进制数据，要使用 io.BytesIO 类
y=io.BytesIO()
y.write(b'letsee')
print(y.getvalue())

'''

11
helloworld
this is a test

nic
e
everybody

b'letsee'

'''

#当你想模拟一个普通的文件的时候 StringIO 和 BytesIO 类是很有用的。 比如，在单元测试中，你可以使用 StringIO 来创建一个包含测试数据的类文件对象， 这个对象可以被传给某个参数为普通文件对象的函数。

#需要注意的是， StringIO 和 BytesIO 实例并没有正确的整数类型的文件描述符。 因此，它们不能在那些需要使用真实的系统级文件如文件，管道或者是套接字的程序中使用。



