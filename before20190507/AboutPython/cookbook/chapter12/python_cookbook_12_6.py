# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/6 5:24 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_6.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# threading.local

# 暂时这样认为吧。threading.local的实例为每个线程维护一个单独的实例字典。所有的普通实例操作比如获取，修改，和删除值仅仅是操作这个字典，每个线程使用一个独立的字典就可以保证数据的隔离了

# 12.5中local实例存了一堆锁对象。12.6中又存了sock对象。看来只要是对象就可以存...意犹未尽


# threading.local最大的用处就是HTTP请求时绑定用户的信息。这样每个用户线程可以非常方便访问各自的资源而互不干扰


from socket import socket,AF_INET,SOCK_STREAM
import threading

class LazyConnection:

    def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
        self.address=address
        self.family=family
        self.type=type
        self.local=threading.local()

    def __enter__(self):
        if hasattr(self.local,"sock"):
            raise RuntimeError("Already conneccted")

        self.local.sock=socket(self.family,self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self,exc_ty,exc_val,tb):
        self.local.sock.close()
        del self.local.sock


from functools import partial

def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host:www.python.org\r\n')
        s.send(b'\r\n')
        resp=b''.join(iter(partial(s.recv,8192),b''))

    print('Got {} bytes'.format(len(resp)))

if __name__ == "__main__":
    conn=LazyConnection(("www.python.org",80))
    t1=threading.Thread(target=test,args=(conn,))
    t2=threading.Thread(target=test,args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


