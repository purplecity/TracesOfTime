# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/30 2:43 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_4.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#线程调度本质上是不确定的
# Lock 对象和 with 语句块一起使用可以保证互斥执行，就是每次只有一个线程可以执行 with 语句包含的代码块。with 语句会在这个代码块执行前自动获取锁，在执行结束后自动释放锁。

import threading

class SharedCounter:
    def __init__(self,initial_value=0):
        self._value=initial_value
        self._value_lock=threading.Lock()

    def incr(self,delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self,delta=1):
        with self._value_lock:
            self._value -= delta

# 为了避免出现死锁的情况，使用锁机制的程序应该设定为每个线程一次只允许获取一个锁
# 而且就使用lock而不是lock.acquire()和lock.release()一起使用
# 一个线程就使用一次锁
# 想要一个线程一次使用多次同一个锁 使用RLOCK。其实就是无需再去获得锁？
# 一个 RLock （可重入锁）可以被同一个线程多次获取，主要用来实现基于监测对象模式的锁定和同步。在使用这种锁的情况下，当锁被持有时，只有一个线程可以使用完整的函数或者类中的方法。


class SharedCounter2:
    _lock=threading.RLock()

    def __init__(self,initial_value=0):
        self._value=initial_value

    def incr(self,delta=1):
        with SharedCounter2._lock:
            self._value += delta

    def decr(self,delta=1):
        with SharedCounter2._lock:
            self.incr(-delta)

# 这个锁可以保证一次只有一个线程可以调用这个类方法。跟标准锁一样的
# 值得一读
# 与一个标准的锁不同的是，已经持有这个锁的方法在调用同样使用这个锁的方法时，无需再次获取锁


# 信号量对象是一个建立在共享计数器基础上的同步原语。如果计数器不为0，with 语句将计数器减1，线程被允许执行。with 语句执行结束后，计数器加１。如果计数器为0，线程将被阻塞，直到其他线程结束将计数器加1。尽管你可以在程序中像标准锁一样使用信号量来做线程同步，但是这种方式并不被推荐，因为使用信号量为程序增加的复杂性会影响程序性能。相对于简单地作为锁使用，信号量更适用于那些需要在线程之间引入信号或者限制的程序。比如，你需要限制一段代码的并发访问量，你就可以像下面这样使用信号量完成：


from threading import Semaphore
import  urllib.request

_fetch_url_sema=Semaphore(5)
def fetch_url(url):
    with _fetch_url_sema:
        return urllib.request.urlopen(url)


