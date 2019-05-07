
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 3:24 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_11_2.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#  创建tcp服务器

# socketserver
from  socketserver import BaseRequestHandler,TCPServer,ThreadingTCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('got connection from',self.client_address)
        while True:
            msg=self.request.recv(8192)
            if not msg: break
            self.request.send(msg)
'''
if  __name__=='__main__':
    serv=TCPServer(("",20000),EchoHandler)
    #serv=ThreadingTCPServer(("",20000),EchoHandler)
    serv.serve_forever()


socketserver 可以让我们很容易的创建简单的TCP服务器。 但是，你需要注意的是，默认情况下这种服务器是单线程的，一次只能为一个客户端连接服务。 如果你想处理多个客户端，可以初始化一个 ForkingTCPServer 或者是 ThreadingTCPServer 对象。


使用fork或线程服务器有个潜在问题就是它们会为每个客户端连接创建一个新的进程或线程。 由于客户端连接数是没有限制的，因此一个恶意的黑客可以同时发送大量的连接让你的服务器奔溃。


如果你担心这个问题，你可以创建一个预先分配大小的工作线程池或进程池。 你先创建一个普通的非线程服务器，然后在一个线程池中使用 serve_forever() 方法来启动它们




if __name__=="__main__":
    from threading import Thread
    NWORKERS=16
    serv=TCPServer(("",20000),EchoHandler)

    for n in range(NWORKERS):
        t=Thread(target=serv.serve_forever())
        t.daemon=True
        t.start()
    serv.serve_forever()

'''

from socket import socket,AF_INET,SOCK_STREAM

def echo_handler(address,client_sock):
    print('got connection from {}'.format(address))
    while True:
        msg=client_sock.recv(8192)
        if not msg: break
        client_sock.sendall(msg)
    client_sock.close()


def echo_server(address,backlog=5):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock,client_addr=sock.accept()
        echo_handler(client_addr,client_sock)

if __name__=="__main__":
    echo_server(("",20000))

