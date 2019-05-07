# 将文件描述符包装成文件对象

# 我猜测就是linux底层文件描述符和文件指针之间的转换

# 一个文件描述符和一个打开的普通文件是不一样的。 文件描
# 述符仅仅是一个由操作系统指定的整数，用来指代某个系统的I/O通道。 如果你碰巧
# 有这么一个文件描述符，你可以通过使用 open() 函数来将其包装为一个Python的文件对象。
# 你仅仅只需要使用这个整数值的文件描述符作为第一个参数来代替文件名即可。

import os
fd=os.open('somefile.txt',os.O_WRONLY|os.O_CREAT)
f=open(fd,'wt')
f.write('helloworld\n')
f.close()

#当高层的文件对象被关闭或者破坏的时候，底层的文件描述符也会被关闭。 如果这个
# 并不是你想要的结果，你可以给 open() 函数传递一个可选的 colsefd=False 。
f=open(fd,'wt',closefd=False)


# 尽管可以将一个已存在的文件描述符包装成一个正常的文件对象， 但是要注意的
# 是并不是所有的文件模式都被支持，并且某些类型的文件描述符
# 可能会有副作用 (特别是涉及到错误处理、文件结尾条件等等的时候)。

#一个操作管道的例子

from socket import socket,AF_INET,SOCK_STREAM

def echo_client(client_sock,addr):
    print('got connection from',addr)

    client_in=open(client_sock.fileno(),'rt',encoding='latin-1',closefd=False)

    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1', closefd=False)

    for line in client_in:
        client_out.write(line)
        client_out.flush()
    client_sock.close()

def echo_server(address):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client,addr=sock.accept()
        echo_client(client,addr)


    