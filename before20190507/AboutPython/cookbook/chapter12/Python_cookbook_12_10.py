# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/6 8:05 PM                               
#  Author           purplecity                                       
#  Name             Python_cookbook_12_10.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#  actor模型
#  不太理解： 简单来讲，一个actor就是一个并发执行的任务，只是简单的执行发送给他的消息任务。队列能并发？ 响应这些消息时，它可能还会给其他actor发送更进一步
# 的消息，actor之间的通信我是单向和异步的。

# 一个线程和一个队列可以很容易的定义actor

from queue import Queue
from threading import Thread,Event

class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mainbox=Queue()

    def send(self,msg):
        self._mainbox.put(msg)

    def recv(self):
        msg=self._mainbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def start(self):
        self._terminated=Event()
        t=Thread(target=self._bootstrap)
        t.daemon=True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        while True:
            msg=self.recv()

# run在 是一直recv  recv在接受哨兵时候回导致_bootstrap的ActorExit。最后set。 joinok

'''
class TaggedActor(Actor):
    def run(self):
        while True:
            tag,*payload=self.recv()
            getattr(self,"do_"+tag)(*payload)

    def do_A(self,x):
        print("running A",x)

    def do_B(self,x,y):
        print("Runing B",x,y)

a=TaggedActor()
a.start()
a.send(("A",1))
a.send(("B",2,3))
'''


class Result:
    def __init__(self):
        self.__evt=Event()
        self.result=None

    def set_result(self,value):
        self.__result=value
        self.__evt.set()


    def result(self):
        self.__evt.wait()
        return self.__result

class Worker(Actor):
    def submit(self,func,*args,**kwargs):
        r=Result()
        self.send((func,args,kwargs,r))
        return r

    def run(self):
        while True:
            func,args,kwargs,r=self.recv()# 阻塞等待 submit
            r.set_result(func(*args,**kwargs))

worker=Worker()
worker.start()
r=worker.submit(pow,3,3) #会被处理
print(r.result())# wait 会被 直到处理完 否则一直阻塞


# 最主要的是  发送一个任务消息概念可以扩展到多进程甚至是大型分布式系统中去。
