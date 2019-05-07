
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 3:56 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_11_3.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

from socketserver import BaseRequestHandler,UDPServer

import time

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('got connection from',self.client_address)
        msg,sock=self.request
        resp=time.ctime()
        sock.sendto(resp.encode("ascii"),self.client_address)

if __name__=="__main__":
    serv=UDPServer(("",20000),TimeHandler)
    serv.serve_forever()

#一个典型的UDP服务器接收到达的数据报(消息)和客户端地址。

'''
 你应该使用socket的 sendto() 和 recvfrom() 方法。 尽管传统的 send() 和 recv() 也可以达到同样的效果， 但是前面的两个方法对于UDP连接而言更普遍。
'''
