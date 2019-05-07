# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 7:57 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_2.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# t_is_alive只是判断或者不活着
# 判断线程是否已经启动

'''

线程的一个关键特性是每个线程都是独立运行且状态不可预测。如果程序中的其他线程需要通过判断某个线程的状态来确定自己下一步的操作，这时线程同步问题就会变得非常棘手。为了解决这些问题，我们需要使用 threading 库中的 Event 对象

#  event.wait(timeout=None)：调用该方法的线程会被阻塞，如果设置了timeout参数，超时后，线程会停止阻塞继续执行
event是全局的。用于线程间通信


1、join ()方法：主线程A中，创建了子线程B，并且在主线程A中调用了B.join()，那么，主线程A会在调用的地方等待，直到子线程B完成操作后，才可以接着往下执行，那么在调用这个线程时可以使用被调用线程的join方法。
原型：join([timeout])
里面的参数时可选的，代表线程运行的最大时间，即如果超过这个时间，不管这个此线程有没有执行完毕都会被回收，然后主线程或函数都会接着执行的。

setDaemon（）可以参考Python文档说明。大概意思就是可以设置setDaemon的参数为True来表示将该线程指定为守护线程，如果参数为False就不指定线程为守护线程。设置setDaemon的参数为True之后。主线程和子线程会同时运行，主线程结束运行后，无论子线程运行与否，都会和主线程一起结束。
意思就是不再去等待子线程

'''

'''
from threading import Thread,Event
import time

def countdown(n,started_evt):
    print("countdown starting")
    started_evt.set()
    while n > 0:
        print("t-minus",n)
        n -= 1
        time.sleep(5)

started_evt=Event()
print('launching countdown')
t=Thread(target=countdown,args=(10,started_evt))
t.setDaemon(True)
t.start()
started_evt.wait()
print('countdown is running')
'''


##event只用于单次。如果想重复使用event使用condition。如果
#只想唤醒单个线程，也最好使用condition
# 值得读


#官方文档中有Lock RLock Timer Barrier Condition Semaphore等object在threading模块
# https://docs.python.org/3/library/threading.html#condition-objects

# 所有关于threading的内容建议读官网

import threading
import time


'''
class PeriodicTimer:
    def __init__(self,interval):
        self._interval=interval
        self._flag=0
        self._cv=threading.Condition()

    def start(self):
        t=threading.Thread(target=self.run)
        t.daemon=True
        t.start()

    def run(self):
        while True: #5s之后唤醒所有等待这个条件变量的线程
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()

    def wait_for_tick(self):
        with self._cv:
            last_flag=self._flag
            while last_flag == self._flag:
                self._cv.wait()

ptimer = PeriodicTimer(5)
ptimer.start()

def countdown(nticks):
    while nticks > 0:
        ptimer.wait_for_tick()
        print("T-minmus",nticks)
        nticks -= 1

def countup(last):
    n=0
    while n<last: #  一直循环一直wait
        ptimer.wait_for_tick()
        print("counting",n)
        n += 1

threading.Thread(target=countdown,args=(10,)).start()
threading.Thread(target=countup,args=(5,)).start()

'''
'''
semaphore是一个内置的计数器

每当调用acquire()时，内置计数器-1
每当调用release()时，内置计数器+1
计数器不能小于0，当计数器为0时，acquire()将阻塞线程直到其他线程调用release()。

'''


def worker(n,sema):
    sema.acquire()
    print("working",n)

sema=threading.Semaphore(0)
nworkers=10

for n in range(nworkers):
    t=threading.Thread(target=worker,args=(n,sema))
    t.start()

sema.release()
sema.release()