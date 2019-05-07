# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/30 2:10 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_3.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

'''
从一个线程向另一个线程发送数据最安全的方式可能就是使用 queue 库中的队列了。创建一个被多个线程共享的 Queue 对象，这些线程通过使用 put() 和 get() 操作来向队列中添加或者删除元素。
'''

from queue import Queue
from threading import Thread

'''
def producer(out_q):
    while True:
        out_q.put("hehe")



def consumer(in_q):
    while True:
        data=in_q.get()

q=Queue()
t1=Thread(target=consumer,args=(q,))
t2=Thread(target=producer,args=(q,))


# Queue 对象已经包含了必要的锁，所以你可以通过它在多个线程间多安全地共享数据

_sentinel=object()
def producer1(out_q):
    while running:
        out_q.put(data)
    out_q.put(_sentinel)

def consumer1(in_q):
    while True:
        data=in_q.get()
        if data is _sentinel:
            in_q.put(_sentinel)
            break

# 消费者在读到这个特殊值之后立即又把它放回到队列中，将之传递下去。这样，所有监听这个队列的消费者线程就可以全部关闭了
#还是不完美毕竟有人抢占



import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._count=0
        self._cv=threading.Condition()

    def put(self,item,priority):
        with self._cv:
            heapq.heappush(self._queue,(-priority,self._count,item))
            self._count += 1
            self._cv.notify()



from queue import Queue
from threading import Thread,Event

def producer(out_q):
    while running:
        evt=Event()
        out_q.put((data,evt))
        evt.wait()

def consumer(in_q):
    while True:
        data,evt=in_q.get() #接收到消息
        evt.set() #完成消息

q=Queue()
t1=Thread(target=producer,args=(q,))
t2=Thread(target=consumer,args=(q,))
t1.start()
t2.start()

'''


'''
使用线程队列有一个要注意的问题是，向队列中添加数据项时并不会复制此数据项，线程间通信实际上是在线程间传递对象引用。如果你担心对象的共享状态，那你最好只传递不可修改的数据结构（如：整型、字符串或者元组）或者一个对象的深拷贝。
毕竟线程间全局共享
'''


#值得读 queue 是线程安全的。但是qsize full empty是不安全的

