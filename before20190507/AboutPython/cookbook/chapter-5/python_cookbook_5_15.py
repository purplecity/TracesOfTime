# 打印不合法的文件名

# 你的程序获取了一个目录中的文件名列表，但是当它试着去打印文
# 件名的时候程序崩溃， 出现了 UnicodeEncodeError 异常和一条奇
# 怪的消息—— surrogates not allowed 。

import os,sys
def bad_filename(filename):
    return repr(filename)[1:-1]


files=os.listdir('.')  #['spam.py', 'b\udce4d.txt', 'foo.txt']
for name in files:
    try:
        print(name)
    except UnicodeDecodeError:
        print(bad_filename(name))


#这一节值得阅读。任何角落都可能是致命而诱惑的

#或者这样处理

def bad_filename(filename):
    temp=filename.encode(sys.getfilesystemencoding(),errors='surrogateescape')
    return temp.decode('latin-1')

'''
surrogateescape:
这种是Python在绝大部分面向OS的API中所使用的错误处理器，
它能以一种优雅的方式处理由操作系统提供的数据的编码问题。
在解码出错时会将出错字节存储到一个很少被使用到的Unicode编码范围内。
在编码时将那些隐藏值又还原回原先解码失败的字节序列。
它不仅对于OS API非常有用，也能很容易的处理其他情况下的编码错误。

'''