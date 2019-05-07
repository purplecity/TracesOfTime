# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 4:40 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_11_9.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# hmac 认证的一个常见使用场景是内部消息通信系统和进程间通信。
# multiprocessing 就是用来干这个的

'''
相关背景:
消息摘要（Message Digest）又称为数字摘要(Digital Digest)。它是一个唯一对应一个消息或文本的固定长度的值，它由一个单向Hash加密函数对消息进行作用而产生。如果消息在途中改变了，则接收者通过对收到消息的新产生的摘要与原摘要比较，就可知道消息是否被改变了。因此消息摘要保证了消息的完整性。 消息摘要采用单向Hash 函数将需加密的明文"摘要"成一串128bit的密文，这一串密文亦称为数字指纹(Finger Print)，它有固定的长度，且不同的明文摘要成密文，其结果总是不同的，而同样的明文其摘要必定一致。这样这串摘要便可成为验证明文是否是"真身"的"指纹"了。

HMAC 算法主要应用于身份验证，用法如下：

1.客户端发出登录请求
2.服务器返回一个随机值，在会话记录中保存这个随机值
3.客户端将该随机值作为密钥，用户密码进行 hmac 运算，递交给服务器
4.服务器读取数据库中的用户密码，利用密钥做和客户端一样的 hmac运算，然后与用户发送的结果比较，如果一致，则用户身份合法。

'''


import hmac ,os
from socket import socket,AF_INET,SOCK_STREAM

def client_authenticate(connection,secret_key):
    message=connection.recv(32)
    hash=hmac.new(secret_key,message)
    digest=hash.digest()
    connection.send(digest)

def server_authenticate(connection,secret_key):
    message=os.urandom(32)
    connection.send(message)
    hash=hmac.new(secret_key,message)
    digest=hash.digest()
    response=connection.recv(len(digest))
    return hmac.compare_digest(digest,response)

secret_key=b'peekaboo'

def echo_handler(client_sock):
    if not server_authenticate(client_sock,secret_key):
        client_sock.close()
        return
    while True:
        msg=client_sock.recv(8192)
        if not msg: break
        client_sock.sendall(msg)
        # This calls send() repeatedly
        #         until all data is sent
        # socket代表着一个连接。发送就是发送到连接的另一端


def  echo_server(address):
    s=socket(AF_INET,SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    while True:
        c,a=s.accept()
        echo_handler(c)

echo_server(("",18000))