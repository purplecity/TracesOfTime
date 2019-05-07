# 增加或改变已经打开文件的编码

'''
已经经过验证
I/O系统由一系列的层次构建而成。你可以试着运行下面这个操作一个文本文件的例子来查看这种层次：

>>> f = open('sample.txt','w')
>>> f
<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
>>> f.buffer
<_io.BufferedWriter name='sample.txt'>
>>> f.buffer.raw
<_io.FileIO name='sample.txt' mode='wb'>
>>>
在这个例子中，io.TextIOWrapper 是一个编码和解码Unicode的文本处理层， io.BufferedWriter 是一个处理二进制数
据的带缓冲的I/O层， io.FileIO 是一个表示操作系统底层文件描述符的原始文件。 增加或改变文本编码会涉及
增加或改变最上面的 io.TextIOWrapper 层。


不能直接修改最顶层，只能用detach断开最顶层然后添加最顶层

>>> f
<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
>>> f = io.TextIOWrapper(f.buffer, encoding='latin-1')
>>> f
<_io.TextIOWrapper name='sample.txt' encoding='latin-1'>
>>> f.write('Hello')
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
结果出错了，因为f的原始值已经被破坏了并关闭了底层的文件。

detach() 方法会断开文件的最顶层并返回第二层，之后最顶层就没什么用了。例如：

>>> f = open('sample.txt', 'w')
>>> f
<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
>>> b = f.detach()
>>> b
<_io.BufferedWriter name='sample.txt'>
>>> f.write('hello')
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
ValueError: underlying buffer has been detached
>>>


一旦断开最顶层后，你就可以给返回结果添加一个新的最顶层。比如：

>>> f = io.TextIOWrapper(b, encoding='latin-1')
>>> f
<_io.TextIOWrapper name='sample.txt' encoding='latin-1'>
>>>

'''

#你想给一个以二进制模式打开的文件添加Unicode编码/解码方式， 可以
# 使用 io.TextIOWrapper() 对象包装它。比如：

import urllib.request,io
u=urllib.request.urlopen('http://www.python.org')
f=io.TextIOWrapper(u,encoding='utf-8')
text=f.read()

'''
如果你想修改一个已经打开的文本模式的文件的编码方式，可以先使用 detach() 方法移除
掉已存在的文本编码层， 并使用新的编码方式代替。下面是一个在 sys.s
tdout 上修改编码方式的例子：
'''

import sys
print(sys.stdout.encoding)
sys.stdout=io.TextIOWrapper(sys.stdout.detach(),encoding='latin-1')
print(sys.stdout.encoding)


#二进制似乎可以直接替换最顶层。文本文件需要先detach，然后encoding
#可以一步操作  sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='ascii',errors='xmlcharrefreplace')