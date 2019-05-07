"""Thread module emulating a subset of Java's threading model."""
import os as _os
import sys as _sys
import _thread

from time import monotonic as _time
from traceback import format_exc as _format_exc
from _weakrefset import WeakSet
from itertools import islice as _islice, count as _count
try:
    from _collections import deque as _deque
except ImportError:
    from collections import deque as _deque

# Note regarding PEP 8 compliant names
#  This threading model was originally inspired by Java, and inherited
# the convention of camelCase function and method names from that
# language. Those original names are not in any imminent danger of
# being deprecated (even for Py3k),so this module provides them as an
# alias for the PEP 8 compliant names
# Note that using the new PEP 8 compliant names facilitates substitution
# with the multiprocessing module, which doesn't provide the old
# Java inspired names.

__all__ = ['get_ident', 'active_count', 'Condition', 'current_thread',
           'enumerate', 'main_thread', 'TIMEOUT_MAX',
           'Event', 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Thread',
           'Barrier', 'BrokenBarrierError', 'Timer', 'ThreadError',
           'setprofile', 'settrace', 'local', 'stack_size']

# Rename some stuff so "from threading import *" is safe
_start_new_thread = _thread.start_new_thread
_allocate_lock = _thread.allocate_lock
_set_sentinel = _thread._set_sentinel #哨兵
get_ident = _thread.get_ident
ThreadError = _thread.error
try:
    _CRLock = _thread.RLock
except AttributeError:
    _CRLock = None
TIMEOUT_MAX = _thread.TIMEOUT_MAX
del _thread

##一切c文件中的方法。见https://docs.python.org/3/library/_thread.html。也说明了Lock是mutex


'''

词语准确性与c中锁的东西:
1 词语准确性:
    一切的锁指锁对象 在c中是pthread_mutex_t,在python是Lock实例。
    没有获得/释放锁这个概念。只有初始化锁,加锁，解锁,销毁锁这样的概念。获取/释放只有获取/释放控制权即获取/释放该锁的控制权这个概念。在python中只有加锁和解锁的概念
    意会:在c中初始化锁就是一个人和一把锁(没锁上)。人对应于线程。锁对应于锁对象。加锁就加加锁。解锁就解锁。销毁锁就是扔掉锁

一个线程可以有多个锁对象--锁的粒度太高并不是好事麻烦

c中：
互斥锁：
对于读者和写者来说。只要有一方获取了锁的控制权，另一方则不能继续获取锁的控制权
读写锁-适合于对数据结构的读次数比写次数多得多的情况.因为,读模式锁定时可以共享,以写模式锁住时意味着独占,所以读写锁又叫共享-独占锁.

pthread_mutex_lock(&rd);
    执行操作
pthread_mutex_unlock(&rd);


在python中是一个类对象。
with some_lock:
    # do something...

some_lock.acquire()
try:
    # do something...
finally:
    some_lock.release()


GIL是全局解释器锁。cpu调度上如果一个线程block 5ms或者执行了多少字节码之后就会调度执行另外的线程是内核级别上的操作我们不能控制
但是Lock实例是用户级的，我们可以控制


循环锁是基于互斥锁构建的。
    加锁：

    1）如果没有任何线程加锁，就直接加锁，并且记录下当前线程的ID；

    2）如果当前线程加过锁了，就不用加锁了，只是将加锁的计数增加1；

    3）如果其他线程加锁了，那么就等待直到加锁成功，后继步骤与第一种情况相同。

    解锁：

    1）如果不是当前线程加的锁或者没有人加锁，那这是错误的调用，直接返回。

    2）如果是当前线程加锁了，将加锁的计数减1.如果计数仍大于0，说明当前线程加了多个锁(减了一次还是1)，直接返回就行了。如果计数为0，说明当前线程只加了一

    次锁，则执行解锁操作。
'''



# Support for profile and trace hooks

_profile_hook = None
_trace_hook = None

def setprofile(func):
    """Set a profile function for all threads started from the threading module.

    The func will be passed to sys.setprofile() for each thread, before its
    run() method is called.

    """
    global _profile_hook
    _profile_hook = func

def settrace(func):
    """Set a trace function for all threads started from the threading module.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.

    """
    global _trace_hook
    _trace_hook = func


# 呀到了非常系统底层的层次。也不影响分析这个python文件。不懂忽略

# Synchronization classes

Lock = _allocate_lock
# Lock也是从c中继承而来的。在threadmodule.c中也有跟_RLock同样的所有方法。Lock()就是获取一把互斥锁实例了

#注意所有英文注释
#下面所有的英文注释描述不准。没有acquired lock  应该是(thread)acquired lock's ownership.也没有release lock  应该是(thread)release lock's ownership




def RLock(*args, **kwargs):
    """Factory function that returns a new reentrant(可重入) lock.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it again
    without blocking; the thread must release it once for each time it has
    acquired it.

    """
    if _CRLock is None:
        return _PyRLock(*args, **kwargs)  # _PyRLock = _RLock就是下面的_RLock类
    return _CRLock(*args, **kwargs)
    #这意味自己写的_RLock要跟c中的RLock一样。就是获得一个RLock实例

class _RLock:
    """This class implements reentrant(可重入) lock objects.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it
    again without blocking; the thread must release it once for each time it
    has acquired it.
    """

    def __init__(self):
        self._block = _allocate_lock()  # 一个Lock实例
        self._owner = None
        self._count = 0
        # 一个普通的锁对象 一个owner线程 一个count计数


    def __repr__(self):
        owner = self._owner
        try:
            owner = _active[owner].name
        except KeyError:
            pass
        return "<%s %s.%s object owner=%r count=%d at %s>" % (
            "locked" if self._block.locked() else "unlocked",
            self.__class__.__module__,
            self.__class__.__qualname__,
            owner,
            self._count,
            hex(id(self))
        )

    def acquire(self, blocking=True, timeout=-1):
        """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab(获取) ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.最后一种情况--多个阻塞等待的线程只有一个acquire了锁的控制权,另外就继续阻塞等待。当然没返回值--准确描述就应该是true或者阻塞。阻塞跟None没关系

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
        me = get_ident()
        if self._owner == me:
            self._count += 1
            return 1
        rc = self._block.acquire(blocking, timeout)
        if rc:
            self._owner = me
            self._count = 1
        return rc

    __enter__ = acquire # __enter__就是获得锁的控制权

    def release(self):
        """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed(只允许其中一个去获得). If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.
        到此为止锁跟c中锁描述一致了

        There is no return value.

        """
        if self._owner != get_ident():
            raise RuntimeError("cannot release un-acquired lock")
        self._count = count = self._count - 1
        if not count:
            self._owner = None
            self._block.release()

    def __exit__(self, t, v, tb):
        self.release()

    # Internal methods used by condition variables
    #下面的方法给condition使用

    def _acquire_restore(self, state):
        self._block.acquire()
        self._count, self._owner = state
        #给定count owner

    def _release_save(self):
        if self._count == 0:
            raise RuntimeError("cannot release un-acquired lock")
        count = self._count
        self._count = 0
        owner = self._owner
        self._owner = None
        self._block.release()
        return (count, owner)
        #记住count owner并清空count owner 彻底释放锁并保存状态

    def _is_owned(self):
        return self._owner == get_ident()

_PyRLock = _RLock

# 以下全是python自己的实现。应该要做到与c相同


class Condition:
    """Class that implements a condition variable.

    A condition variable allows one or more threads to wait until they are
    notified by another thread.

    If the lock argument is given and not None, it must be a Lock or RLock
    object, and it is used as the underlying lock. Otherwise, a new RLock object
    is created and used as the underlying lock.

    """

    def __init__(self, lock=None):
        if lock is None:
            lock = RLock()
        self._lock = lock #condition的底层锁
        # Export the lock's acquire() and release() methods
        self.acquire = lock.acquire
        self.release = lock.release
        # If the lock defines _release_save() and/or _acquire_restore(),
        # these override the default implementations (which just call
        # release() and acquire() on the lock).  Ditto for _is_owned().

        #之所以try -- lock可能是Lock也可能是RLock
        try:
            self._release_save = lock._release_save
        except AttributeError:
            pass
        try:
            self._acquire_restore = lock._acquire_restore
        except AttributeError:
            pass
        try:
            self._is_owned = lock._is_owned
        except AttributeError:
            pass
        self._waiters = _deque()
        #一个RLock或者Lock 一些方法 一个deque

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    #RLock或者Lock的enter exit就是acquire release

    def __repr__(self):
        return "<Condition(%s, %d)>" % (self._lock, len(self._waiters))

    def _release_save(self):
        self._lock.release()           # No state to save

    def _acquire_restore(self, x):
        self._lock.acquire()           # Ignore saved state

    def _is_owned(self):
        # Return True if lock is owned by current_thread.
        # This method is called only if _lock doesn't have _is_owned().就是单纯的Lock对象才会调用这个方法
        #真怪异。没能获取到锁控制权是true。能够获取到锁控制权就是false。
        if self._lock.acquire(0):
            self._lock.release()
            return False
        else:
            return True

    #截止到目前为止 官方文档上 关于RLOCK和LOCK就只有acquire和release方法。condition中也没有_release_save _acquire_restore _is_owned这三个方法
    #这三个方法设置的有点怪异。为什么不把这三个函数的定义放在init中except中呢？
    #因为经过测试。如果底层锁是Lock实例。就会调用自己定义的这三个方法。如果底层锁是c的RLock还是自己
    #定义的RLock实例就会调用相应的这三种方法。因为C中RLock也有这三种方法功能返回值都是一样的

    def wait(self, timeout=None):
        """Wait until notified or until a timeout occurs.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method releases the underlying lock, and then blocks until it is
        awakened by a notify() or notify_all() call for the same condition
        variable in another thread, or until the optional timeout occurs. Once
        awakened or timed out, it re-acquires the lock and returns.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        When the underlying lock is an RLock, it is not released using its
        release() method, since this may not actually unlock the lock when it
        was acquired multiple times recursively. Instead, an internal interface
        of the RLock class is used, which really unlocks it even when it has
        been recursively acquired several times. Another internal interface is
        then used to restore the recursion level when the lock is reacquired.

        """
        if not self._is_owned(): #要想不raise,is_owned为true。如果init是Lock:acquire(0)为false没有等待,要么就是Lock对象accquire到锁控制权了,也有可能获取不到锁控制权即别的线程占有着锁控制权---所以python官方
        #忽略这一种特殊情况,RLock:当前线程等于RLock的owner。
        #RLock中的owner等于当前线程当仅当acquire调用即-RLock中的lock对象调用了acquire。而且是调用成功了
            raise RuntimeError("cannot wait on un-acquired lock")
        waiter = _allocate_lock() #又创建一个锁Lock对象
        waiter.acquire() #获得新创建锁的控制权
        self._waiters.append(waiter) #把锁放到deque中
        saved_state = self._release_save()#如果底层锁是Lock对象 这三个函数就调用condition定义的函数。否则就调用底层锁对应的这三个函数。如果是RLock(c或者自己定义的RLock)就保存锁实例的状态。
        gotit = False
        try:    # restore state no matter what (e.g., KeyboardInterrupt)
            if timeout is None:
                waiter.acquire()#因为已经获取过一次锁的控制权了。所以会阻塞在这。直到其他线程释放该锁的控制权。
                gotit = True
            else:
                if timeout > 0:
                    gotit = waiter.acquire(True, timeout) # 阻塞等待一段时间
                else:
                    gotit = waiter.acquire(False) #不阻塞立即返回
            return gotit
        finally:
            self._acquire_restore(saved_state) #获取底层锁，并重置锁对象的内部状态
            if not gotit: #gotit为true的通知线程调用notify不用做。因为调用notify的线程释放锁的控制权的同时还会删除这个锁对象
                try:
                    self._waiters.remove(waiter) # gotit当仅当设置了阻塞时间或者不阻塞获取不到锁的控制权才返回false。
                    #timeout时间内等待不到意味着别的程序没有释放锁的控制权。自己删除掉。
                except ValueError:
                    pass
    #wait到此为止的作用就是在获取底层锁的控制权前提下，然后创建一把锁A并获取锁的控制权。释放底层锁的控制权。再次尝试A的控制权-一直阻塞或者阻塞一段时间或者不阻塞
    #等待通知线程获取到底层锁的控制权---dosomthing--然后释放这个A的控制权。然后调用wait的线程重新获得A的控制权。return true后者false
    #关键是别人释放了这个wait也不能做啥事,这个wait返回的是true或者false。估计只有加在wait语句前后的代码才有效

    #请注意 wait中的临时创建的锁。在wait函数执行完后会被垃圾回收，因为是临时变量。从而多次wait没毛病
    def wait_for(self, predicate, timeout=None):
        """Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.

        """
        endtime = None
        waittime = timeout
        result = predicate()
        while not result:  #其实就是连续wait一个timeout。因为下面的wait如果timeout时间内没有wait到的话-即没有获取到底层锁的控制权循环也就break了。这里的重点是for 如果在waittime时间内获取到了控制权而且函数还是不为真就继续wait。但是wait的时间还是不超过timeout。
            if waittime is not None:
                if endtime is None:
                    endtime = _time() + waittime
                else:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
            self.wait(waittime)
            result = predicate()
        return result

    def notify(self, n=1): #一般是通知线程调用。释放 等待线程创建的锁 的控制权
        """Wake up one or more threads waiting on this condition, if any.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method wakes up at most n of the threads waiting for the condition
        variable; it is a no-op if no threads are waiting.

        """
        if not self._is_owned(): #必须要获得底层锁  调用这也也要释放底层锁的控制权自然是with搭配最好
            raise RuntimeError("cannot notify on un-acquired lock")
        all_waiters = self._waiters
        waiters_to_notify = _deque(_islice(all_waiters, n))
        if not waiters_to_notify:
            return
        for waiter in waiters_to_notify:
            waiter.release()
            try:
                all_waiters.remove(waiter)
            except ValueError:
                pass

    def notify_all(self):
        """Wake up all threads waiting on this condition.

        If the calling thread has not acquired the lock when this method
        is called, a RuntimeError is raised.

        """
        self.notify(len(self._waiters))

    notifyAll = notify_all

'''

example of condition:
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv:
    	logging.debug('Consumer waiting ...')
        cv.wait()
        logging.debug('Consumer consumed the resource')

def producer(cv):
    logging.debug('Producer thread started ...')
    with cv:
        logging.debug('Making resource available')
        logging.debug('Notifying to all consumers')
        cv.notifyAll()

if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    pd.start()

'''



class Semaphore:
    """This class implements semaphore objects.

    Semaphores manage a counter representing the number of release() calls minus
    the number of acquire() calls, plus an initial value. The acquire() method
    blocks if necessary until it can return without making the counter
    negative. If not given, value defaults to 1.

    """

    # After Tim Peters' semaphore class, but not quite the same (no maximum)

    def __init__(self, value=1):
        if value < 0:
            raise ValueError("semaphore initial value must be >= 0")
        self._cond = Condition(Lock())
        self._value = value

    def acquire(self, blocking=True, timeout=None):
        """Acquire a semaphore, decrementing the internal counter by one.

        When invoked without arguments: if the internal counter is larger than
        zero on entry, decrement it by one and return immediately. If it is zero
        on entry, block, waiting until some other thread has called release() to
        make it larger than zero(release的话会+1然后notfy). This is done with proper interlocking so that
        if multiple acquire() calls are blocked, release() will wake exactly one
        of them up. The implementation may pick one at random, so the order in
        which blocked threads are awakened should not be relied on. There is no
        return value in this case.

        When invoked with blocking set to true, do the same thing as when called
        without arguments, and return true.

        When invoked with blocking set to false, do not block. If a call without
        an argument would block, return false immediately; otherwise, do the
        same thing as when called without arguments, and return true.

        When invoked with a timeout other than None, it will block for at
        most timeout seconds.  If acquire does not complete successfully in
        that interval, return false.  Return true otherwise.

        """
        if not blocking and timeout is not None:
            raise ValueError("can't specify timeout for non-blocking acquire")
        rc = False
        endtime = None
        with self._cond: #条件变量底层锁的acquire release
            while self._value == 0:
                if not blocking:
                    break
                if timeout is not None:
                    if endtime is None:
                        endtime = _time() + timeout
                    else:
                        timeout = endtime - _time()
                        if timeout <= 0:
                            break
                self._cond.wait(timeout)  #跟wait_for一样。阻塞一段时间。没人调用release就条件变量自己释放锁对象
            #wait 检测时否已经拥有锁的控制权了。创建新锁A。获得A的控制权，释放底层锁。再次请求获得A的控制权而阻塞--等待notify
            else:
                self._value -= 1
                rc = True
        return rc
        #value 不为0就减1  到0 的时候就相当于self._cond.wait_for(timeout)

    __enter__ = acquire

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        """
        with self._cond: #条件变量底层锁的acquire release
            self._value += 1
            self._cond.notify() #把条件变量中的锁deque释放一个锁控制权,并删除一个锁对象。

    def __exit__(self, t, v, tb):
        self.release()

    #呀。 信号量就是一个典型的用条件变量的生产者消费者模型。 消费者线程wait 生产者线程这release。
    # 信号量作用：互斥锁 同时只允许一个线程更改数据，而Semaphore是同时允许一定数量的线程更改数据
    #每次有线程acquire时。count-1 。直到为0时阻塞等待其他线程release。其实就是控制线程的数量的

class BoundedSemaphore(Semaphore):
    """Implements a bounded semaphore.

    A bounded semaphore checks to make sure its current value doesn't exceed its
    initial value. If it does, ValueError is raised. In most situations
    semaphores are used to guard resources with limited capacity.

    If the semaphore is released too many times it's a sign of a bug. If not
    given, value defaults to 1.

    Like regular semaphores, bounded semaphores manage a counter representing
    the number of release() calls minus the number of acquire() calls, plus an
    initial value. The acquire() method blocks if necessary until it can return
    without making the counter negative. If not given, value defaults to 1.

    """

    def __init__(self, value=1):
        Semaphore.__init__(self, value)
        self._initial_value = value

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        If the number of releases exceeds the number of acquires,
        raise a ValueError.

        """
        with self._cond:
            if self._value >= self._initial_value:
                raise ValueError("Semaphore released too many times")
            self._value += 1
            self._cond.notify()
            #就是保障release的时候value不超过规定值。这个比semaphore更好些

'''
    import threading,time
    def run(n):
        with semaphore:
            time.sleep(1)
            print("yunxing xiancheng")
    semaphore = threading.BoundedSemaphore(5)
    for i in range(20):
        t = threading.Thread(target = run,args=(i,))
        t.start()

'''




class Event:
    """Class implementing event objects.

    Events manage a flag that can be set to true with the set() method and reset
    to false with the clear() method. The wait() method blocks until the flag is
    true.  The flag is initially false.

    """

    # After Tim Peters' event class (without is_posted())

    def __init__(self):
        self._cond = Condition(Lock())
        self._flag = False

    def _reset_internal_locks(self):
        # private!  called by Thread._reset_internal_locks by _after_fork()
        self._cond.__init__(Lock())

    def is_set(self):
        """Return true if and only if the internal flag is true."""
        return self._flag

    isSet = is_set

    def set(self):
        """Set the internal flag to true.

        All threads waiting for it to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
        with self._cond:
            self._flag = True
            self._cond.notify_all()  #唤醒所有的wait线程--拥有self.cond._waiters中任意一个锁实例的线程都会被唤醒

    def clear(self):
        """Reset the internal flag to false.

        Subsequently, threads calling wait() will block until set() is called to
        set the internal flag to true again.

        """
        with self._cond:
            self._flag = False

    def wait(self, timeout=None):
        """Block until the internal flag is true.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread calls set() to set the flag to true, or until
        the optional timeout occurs. 嗯对于event实例来说的化能让为ture的只有set方法可以了。

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        This method returns the internal flag on exit, so it will always return
        True except if a timeout is given and the operation times out.还好有个except

        """
        with self._cond:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait(timeout)  #条件变量的操作又来了。因为这里with是获取了条件变量底层锁的控制权而进来。但是wait的时候已经释放了条件变量底层锁的控制权。所以其他获取底层锁的控制权的方法可以用了比如set和clear
            return signaled

#Event关于官网的描述This is one of the simplest mechanisms for communication between threads: one thread signals an event and other threads wait for it.
#果然基础最重要 event真的好简单。



'''

import threading,time

event=threading.Event()

'''标志位设定，代表绿灯，直接通行；标志位被清空，代表红灯；wait()等待变绿灯'''
def lighter():
    '''0<count<5为绿灯，5<count<=10为红灯，count>10重置标志位'''
    event.set()
    count=1
    while True:
        if count>5 and count<=10:
            event.clear()
            print("\033[1;41m red light is on \033[0m")

        elif count>10:
            event.set()
            count=1
        else:
            print("\033[1;42m green light is on \033[0m")
        time.sleep(1)
        count+=1

def car(name):
    '''红灯停，绿灯行'''
    while True:
        if event.is_set():
            print("[%s] is running..."%name)
            time.sleep(0.25)
        else:
            print("[%s] sees red light,need to wait three seconds"%name)
            event.wait()
            print("\033[1;34;40m green light is on,[%s]start going \033[0m"%name)

light=threading.Thread(target=lighter,)
light.start()

car1=threading.Thread(target=car,args=("Xiaoxiong",))
car1.start()

'''


# A barrier class.  Inspired in part by the pthread_barrier_* api and
# the CyclicBarrier class from Java.  See
# http://sourceware.org/pthreads-win32/manual/pthread_barrier_init.html and
# http://java.sun.com/j2se/1.5.0/docs/api/java/util/concurrent/
#        CyclicBarrier.html
# for information.
# We maintain two main states, 'filling' and 'draining' enabling the barrier
# to be cyclic.  Threads are not allowed into it until it has fully drained
# since the previous cycle.  In addition, a 'resetting' state exists which is
# similar to 'draining' except that threads leave with a BrokenBarrierError,
# and a 'broken' state in which all threads get the exception.

#参考http://timd.cn/python/threading/barrier/
class Barrier:
    """Implements a Barrier.

    Useful for synchronizing a fixed number of threads at known synchronization
    points.  Threads block on 'wait()' and are simultaneously once they have all
    made that call.

    """

    def __init__(self, parties, action=None, timeout=None):
        """Create a barrier, initialised to 'parties' threads.

        'action' is a callable which, when supplied, will be called by one of
        the threads after they have all entered the barrier and just prior to
        releasing them all. If a 'timeout' is provided, it is uses as the
        default for all subsequent 'wait()' calls.

        """
        self._cond = Condition(Lock())
        self._action = action
        self._timeout = timeout
        self._parties = parties #the number of threads required to trip the barrier 栅栏放栅的数量
        self._state = 0 #0 filling, 1, draining, -1 resetting, -2 broken
        self._count = 0

    def wait(self, timeout=None):
        """Wait for the barrier.

        When the specified number of threads have started waiting, they are all
        simultaneously awoken. If an 'action' was provided for the barrier, one
        of the threads will have executed that callback prior to returning.
        Returns an individual index number from 0 to 'parties-1'.

        """
        if timeout is None:
            timeout = self._timeout
        with self._cond:
            self._enter() # Block while the barrier drains.
            index = self._count
            self._count += 1
            try:
                if index + 1 == self._parties:
                    # We release the barrier
                    self._release()
                else:
                    # We wait until someone releases us
                    self._wait(timeout)
                return index
            finally:
                self._count -= 1
                # Wake up any threads waiting for barrier to drain.
                self._exit()

    # Block until the barrier is ready for us, or raise an exception
    # if it is broken.
    def _enter(self):
        while self._state in (-1, 1):
            # It is draining or resetting, wait until done
            self._cond.wait()
        #see if the barrier is in a broken state
        if self._state < 0:
            raise BrokenBarrierError
        assert self._state == 0

    # Optionally run the 'action' and release the threads waiting
    # in the barrier.
    def _release(self):
        try:
            if self._action:
                self._action()
            # enter draining state
            self._state = 1
            self._cond.notify_all()
        except:
            #an exception during the _action handler.  Break and reraise
            self._break()
            raise

    # Wait in the barrier until we are released.  Raise an exception
    # if the barrier is reset or broken.
    def _wait(self, timeout):
        if not self._cond.wait_for(lambda : self._state != 0, timeout):
            #timed out.  Break the barrier
            self._break()
            raise BrokenBarrierError
        if self._state < 0:
            raise BrokenBarrierError
        assert self._state == 1

    # If we are the last thread to exit the barrier, signal any threads
    # waiting for the barrier to drain.
    def _exit(self):
        if self._count == 0:
            if self._state in (-1, 1):
                #resetting or draining
                self._state = 0
                self._cond.notify_all()

    def reset(self):
        """Reset the barrier to the initial state.

        Any threads currently waiting will get the BrokenBarrier exception
        raised.

        """
        with self._cond:
            if self._count > 0:
                if self._state == 0:
                    #reset the barrier, waking up threads
                    self._state = -1
                elif self._state == -2:
                    #was broken, set it to reset state
                    #which clears when the last thread exits
                    self._state = -1
            else:
                self._state = 0
            self._cond.notify_all() #通知所有调用了_cond.wait()函数的所有线程可以获取_cond.wait创建的新锁的控制权了。当然但是还是最终只有一个线程获取到_cond底层锁的控制权

    def abort(self):
        """Place the barrier into a 'broken' state.

        Useful in case of error.  Any currently waiting threads and threads
        attempting to 'wait()' will have BrokenBarrierError raised.

        """
        with self._cond:
            self._break()  #通知所有调用了_cond.wait()函数的所有线程可以获取_cond.wait创建的新锁的控制权了。当然但是还是最终只有一个线程获取到_cond底层锁的控制权
            #barrier实例把自己的状态设置成-2 并notify_all
    def _break(self):
        # An internal error was detected.  The barrier is set to
        # a broken state all parties awakened.
        self._state = -2
        self._cond.notify_all()

    @property
    def parties(self):
        """Return the number of threads required to trip the barrier."""
        return self._parties

    @property
    def n_waiting(self):
        """Return the number of threads currently waiting at the barrier."""
        # We don't need synchronization here since this is an ephemeral result
        # anyway.  It returns the correct value in the steady state.
        if self._state == 0:
            return self._count
        return 0

    @property
    def broken(self):
        """Return True if the barrier is in a broken state."""
        return self._state == -2


#所以假设init参数parties为3  action随意  timeout为None wait参数为None开始模拟。然后恰好用=parties数量的线程都开始调用wait来理解。就开窍了


'''
Barrier类完整分析:
saimaZhalan(赛马栅栏) = Barrier(4,action=随意,timeout=5s) 假设有10个线程(从A-J)可能调用wait(init中有timeout这里就没必要了)
每个线程关注的是count state 以及自己调用的临时变量index---终于全部理解了---这个简单而情况复杂的代码


首先--词语准确性。没有屏障,进入屏障这一说。只有赛马栅栏,通过栅栏这一说。马等同于线程。栅栏等于Barrier实例。赛马有三种操作。1 马想通过栅栏,栅栏让马准备或者等待,2栅栏放行,3马通过栅栏开始跑。那么作用---就是线程之间互相等待,然后通过栅栏就干事,线程之间用栅栏即Barrier实例共享来实现这个等待操作
然后--按照官网的说法(This class provides a simple synchronization primitive for use by a fixed number of threads
that need to wait for each other. Each of the threads tries to pass the barrier by calling the wait() method
and will block until all of the threads have made their wait() calls. At this point, the threads are released simultaneously.
The barrier can be reused any number of times for the same number of threads.---重点是threads need to wait for each other)以最正常的流程走。即10个线程依次调用wait。观察Barrier实例的count state 以及各自线程调用wait方法时临时的index值。
最后--全解析


栅栏四种状态-- 0 初始化状态--等待准备的马达到parties(可能有准备马,一定没有等待马) 1 放行状态 -1 重置状态  -2 损坏状态(必定没有准备的等待的马--就是没有阻塞的马因为都会被notify)
1.马想通过栅栏而栅栏让马准备或者等待(准备和等待注意区分)---线程调用栅栏实例的wait方法想去通过栅栏。栅栏通过_enter(只出现在栅栏处于重置状态或者栅栏处于放行状态--那就让这两个操作搞完先)让马等待和_wait(这个会让栅栏的count+1.栅栏因此记住有多少匹马准备好了)让马准备.
2.栅栏放行---栅栏看到处于_wait准备的马中达到足够parties数量。就让达到parties数量的那匹马通过调用栅栏的_release把栅栏state标记为1---表示栅栏处于放行状态--去放行所有的准备好的马
3.马通过栅栏开始跑---通过调用栅栏的_exit方法跑,每跑出去一匹马栅栏都会count-1。最后一匹马跑出去的时候(count=0了)会把栅栏state标记为0--并通过notfiy_all通知让所有处于_enter等待的马表示你们可以开始准备了

另外两种操作
破损:上帝视角abort或者_wait超时马不耐烦说这个栅栏破了:通知所有马栅栏损坏了并标记栅栏为损坏状态。导致跑到上所有准备和等待通过的马(_enter,_wait阻塞下的线程)全都懵逼不跑了 (raise BrokenBarrierError)。
而且这两个破损操作的话,因为state=-2都raise BrokenBarrierError 除非上帝视角主动reset不然栅栏一直都是坏的

关于reset:官方建议Note that using this function may can require some external synchronization if there are other threads whose state is unknown. If a barrier is broken it
 may be better to just leave it and create a new one.因为调用会有什么样的结果实在是太复杂了。干脆没破损直接就不操作这个。破损了就重新创建新的实例对象完事。尼玛

'''
上帝视角reset:
如果count=0 --- 没有阻塞的马--没有马-notify必定没有意义因为没有阻塞的马 和初始化栅栏操作state=0没问题

    栅栏状态1: 1不可能因为这表示放行状态且没放行完count就不可能等于0了。
    栅栏状态-2: 如果栅栏是损坏状态必定没有准备和等待的马因为都会被notify。再notify也没卵用。但是此种情况初始化栅栏还是有用
    栅栏状态0:如果是放行完后变成状态0的由于已经notyfy_all了所以没有_enter等待的马了。如果是一开始的状态0而且线程也无聊的调用reset
            也不会变成_enter等待因为会变成_wait准备。所以对栅栏状态0此刻没有_wait和_enter的马你notify_all没卵用---推出:栅栏0一定没有等待的马但是可能有准备的马
            此种情况重复初始化栅栏没卵用。notify也没卵用
    栅栏状态-1: 已经调用过reset了。notify必定没卵用。初始化栅栏有用


如果有_wait准备的马即count>0,
    栅栏状态1: 这里官方忽略了一种情况即栅栏处于放行状态但是马还没都跑出去--假设调用reset的线程在调用release的线程之后拿到底层锁那么这种情况notify_all等于没用因为已经释放所有各自线程新创建的锁了state还是1也就是根本没有重置此
种情况也就是说---栅栏处于放行状态在被呼唤重置时不叼调用的线程不会被重置为-1。
    栅栏状态-2:损坏状态 必然没有阻塞的马。notity没用。设置成-1.有问题。因为新来的马看到-1会一直_enter等待阻塞。要别的马去release。所以官方建议直接创建新的
    栅栏状态0: 设置成重置状态有用notify有用。所有_wait的马都会raise BrokenBarrierError
    栅栏状态-1: 已经调用过reset了。notify必定没卵用。set也没卵用




#到目前为止的总结。Lock是最基本的对象 RLock是用了Lock。Condition是用了RLock和Lock  semaphore和event Barrier用了condition
#但是只有Lock RLock Condition semaphore可以用with来操作

# exception raised by the Barrier class
class BrokenBarrierError(RuntimeError):
    pass

'''







# Helper to generate new thread names
_counter = _count().__next__
_counter() # Consume 0 so first non-main thread has id 1.
def _newname(template="Thread-%d"):
    return template % _counter()

# Active thread administration
_active_limbo_lock = _allocate_lock()
_active = {}    # maps thread id to Thread object
_limbo = {}  #Thread实例作为key和value
_dangling = WeakSet() #保存Thread实例的弱引用


#这个类的作用
#很简单：“保存元素弱引用的集合类。元素被回收，集合会把它
#删除。”如果一个类需要知道所有实例，一种好的方案是创建一个
#WeakSet 类型的类属性，保存实例的引用。如果使用常规的 set，实例
#永远不会被垃圾回收，因为类中有实例的强引用，而类存在的时间与
#Python 进程一样长，除非显式删除类。


# Main class for threads

class Thread:
    """A class that represents a thread of control.

    This class can be safely subclassed in a limited fashion. There are two ways
    to specify the activity: by passing a callable object to the constructor, or
    by overriding the run() method in a subclass.



    """

    _initialized = False
    # Need to store a reference to sys.exc_info for printing
    # out exceptions when a thread tries to use a global var. during interp.
    # shutdown and thus raises an exception about trying to perform some
    # operation on/with a NoneType
    _exc_info = _sys.exc_info #类属性 元组 exception type  value  traceback
    # Keep sys.exc_clear too to clear the exception just before
    # allowing .join() to return.
    #XXX __exc_clear = _sys.exc_clear

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is the argument tuple for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        assert group is None, "group argument must be None for now"
        if kwargs is None:
            kwargs = {}
        self._target = target
        self._name = str(name or _newname())
        self._args = args
        self._kwargs = kwargs
        if daemon is not None:
            self._daemonic = daemon
        else:
            self._daemonic = current_thread().daemon #current_thread()返回当前线程 .daemon返回当前线程的daemon属性
        self._ident = None
        self._tstate_lock = None
        self._started = Event()
        self._is_stopped = False
        self._initialized = True
        # sys.stderr is not stored in the class like
        # sys.exc_info since it can be changed between instances
        self._stderr = _sys.stderr  #实例属性
        # For debugging and _after_fork()
        _dangling.add(self) #保存自己实例的弱引用

    def _reset_internal_locks(self, is_alive):
        # private!  Called by _after_fork() to reset our internal locks as
        # they may be in an invalid state leading to a deadlock or crash.
        self._started._reset_internal_locks()
        if is_alive:
            self._set_tstate_lock()
        else:
            # The thread isn't alive after fork: it doesn't have a tstate
            # anymore.
            self._is_stopped = True
            self._tstate_lock = None

    def __repr__(self):
        assert self._initialized, "Thread.__init__() was not called"
        status = "initial"
        if self._started.is_set():
            status = "started"
        self.is_alive() # easy way to get ._is_stopped set when appropriate
        if self._is_stopped:
            status = "stopped"
        if self._daemonic:
            status += " daemon"
        if self._ident is not None:
            status += " %s" % self._ident
        return "<%s(%s, %s)>" % (self.__class__.__name__, self._name, status)

    def start(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:
            raise RuntimeError("thread.__init__() not called")

        if self._started.is_set():
            raise RuntimeError("threads can only be started once")
        with _active_limbo_lock:
            _limbo[self] = self #保存的只是Thread实例
        try:
            _start_new_thread(self._bootstrap, ())

            '''
            _start_new_thread(self._bootstrap, ()) runs self._bootstrap() (in a new thread) which
             calls self._bootstrap_inner() where self._started is set.
            '''

            '''
            官方描述--_thread.start_new_thread(function, args[, kwargs])
            Start a new thread and return its identifier. The thread executes the function function
            with the argument list args (which must be a tuple). The optional kwargs argument specifies
             a dictionary of keyword arguments. When the function returns, the thread silently exits.
             When the function terminates with an unhandled exception, a stack trace is printed and then
             the thread exits (but other threads continue to run).
            '''
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def _bootstrap(self):
        # Wrapper around the real bootstrap code that ignores
        # exceptions during interpreter cleanup.  Those typically
        # happen when a daemon thread wakes up at an unfortunate
        # moment, finds the world around it destroyed, and raises some
        # random exception *** while trying to report the exception in
        # _bootstrap_inner() below ***.  Those random exceptions
        # don't help anybody, and they confuse users, so we suppress
        # them.  We suppress them only when it appears that the world
        # indeed has already been destroyed, so that exceptions in
        # _bootstrap_inner() during normal business hours are properly
        # reported.  Also, we only suppress them for daemonic threads;
        # if a non-daemonic encounters this, something else is wrong.
        try:
            self._bootstrap_inner()
        except:
            if self._daemonic and _sys is None:
                return
            raise

    def _set_ident(self):
        self._ident = get_ident()

    def _set_tstate_lock(self):
        """
        Set a lock object which will be released by the interpreter when
        the underlying thread state (see pystate.h) gets deleted.
        """
        self._tstate_lock = _set_sentinel()
        self._tstate_lock.acquire()

    def _bootstrap_inner(self):
        try:
            self._set_ident()
            self._set_tstate_lock()
            self._started.set()
            with _active_limbo_lock:
                _active[self._ident] = self  #这个是真正对应了子线程号为key Thread实例为value
                del _limbo[self] #微妙但不值得注意

            if _trace_hook:
                _sys.settrace(_trace_hook)
            if _profile_hook:
                _sys.setprofile(_profile_hook)

            try:
                self.run()  #如果是直接创建的Thread类 实例start函数最终会调用run函数 run函数调用target函数
                #如果是继承来的类。类要覆盖run方法。这样实例start函数会调用自己类重写的run函数
            except SystemExit:
                pass
            except:
                # If sys.stderr is no more (most likely from interpreter
                # shutdown) use self._stderr.  Otherwise still use sys (as in
                # _sys) in case sys.stderr was redefined since the creation of
                # self.
                if _sys and _sys.stderr is not None:
                    print("Exception in thread %s:\n%s" %
                          (self.name, _format_exc()), file=_sys.stderr)
                elif self._stderr is not None:
                    # Do the best job possible w/o a huge amt. of code to
                    # approximate a traceback (code ideas from
                    # Lib/traceback.py)
                    exc_type, exc_value, exc_tb = self._exc_info()
                    try:
                        print((
                            "Exception in thread " + self.name +
                            " (most likely raised during interpreter shutdown):"), file=self._stderr)
                        print((
                            "Traceback (most recent call last):"), file=self._stderr)
                        while exc_tb:
                            print((
                                '  File "%s", line %s, in %s' %
                                (exc_tb.tb_frame.f_code.co_filename,
                                    exc_tb.tb_lineno,
                                    exc_tb.tb_frame.f_code.co_name)), file=self._stderr)
                            exc_tb = exc_tb.tb_next
                        print(("%s: %s" % (exc_type, exc_value)), file=self._stderr)
                        self._stderr.flush()
                    # Make sure that exc_tb gets deleted since it is a memory
                    # hog; deleting everything else is just for thoroughness
                    finally:
                        del exc_type, exc_value, exc_tb
            finally:
                # Prevent a race in
                # test_threading.test_no_refcycle_through_target when
                # the exception keeps the target alive past when we
                # assert that it's dead.
                #XXX self._exc_clear()
                pass
        finally:
            with _active_limbo_lock:
                try:
                    # We don't call self._delete() because it also
                    # grabs _active_limbo_lock.
                    del _active[get_ident()]
                except:
                    pass

    def _stop(self):
        # After calling ._stop(), .is_alive() returns False and .join() returns
        # immediately.  ._tstate_lock must be released before calling ._stop().
        #
        # Normal case:  C code at the end of the thread's life
        # (release_sentinel in _threadmodule.c) releases ._tstate_lock, and
        # that's detected by our ._wait_for_tstate_lock(), called by .join()
        # and .is_alive().  Any number of threads _may_ call ._stop()
        # simultaneously (for example, if multiple threads are blocked in
        # .join() calls), and they're not serialized.  That's harmless -
        # they'll just make redundant rebindings of ._is_stopped and
        # ._tstate_lock.  Obscure:  we rebind ._tstate_lock last so that the
        # "assert self._is_stopped" in ._wait_for_tstate_lock() always works
        # (the assert is executed only if ._tstate_lock is None).
        #
        # Special case:  _main_thread releases ._tstate_lock via this
        # module's _shutdown() function.
        lock = self._tstate_lock
        if lock is not None:
            assert not lock.locked()
        self._is_stopped = True
        self._tstate_lock = None

    def _delete(self):
        "Remove current thread from the dict of currently running threads."
        with _active_limbo_lock:
            del _active[get_ident()]
            # There must not be any python code between the previous line
            # and after the lock is released.  Otherwise a tracing function
            # could try to acquire the lock again in the same thread, (in
            # current_thread()), and would block.

    def join(self, timeout=None):
        """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        is_alive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if not self._started.is_set():
            raise RuntimeError("cannot join thread before it is started")
        if self is current_thread():
            raise RuntimeError("cannot join current thread")

        if timeout is None:
            self._wait_for_tstate_lock()
        else:
            # the behavior of a negative timeout isn't documented, but
            # historically .join(timeout=x) for x<0 has acted as if timeout=0
            self._wait_for_tstate_lock(timeout=max(timeout, 0))

    def _wait_for_tstate_lock(self, block=True, timeout=-1):
        # Issue #18808: wait for the thread state to be gone.
        # At the end of the thread's life, after all knowledge of the thread
        # is removed from C data structures, C code releases our _tstate_lock.
        # This method passes its arguments to _tstate_lock.acquire().
        # If the lock is acquired, the C code is done, and self._stop() is
        # called.  That sets ._is_stopped to True, and ._tstate_lock to None.
        lock = self._tstate_lock
        if lock is None:  # already determined that the C code is done
            assert self._is_stopped
        elif lock.acquire(block, timeout):
            lock.release()
            self._stop()

    @property
    def name(self):
        """A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        """
        assert self._initialized, "Thread.__init__() not called"
        return self._name

    @name.setter
    def name(self, name):
        assert self._initialized, "Thread.__init__() not called"
        self._name = str(name)

    @property
    def ident(self):
        """Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.

        """
        assert self._initialized, "Thread.__init__() not called"
        return self._ident

    def is_alive(self):
        """Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        """
        assert self._initialized, "Thread.__init__() not called"
        if self._is_stopped or not self._started.is_set():
            return False
        self._wait_for_tstate_lock(False)
        return not self._is_stopped

    def isAlive(self):
        """Return whether the thread is alive.

        This method is deprecated, use is_alive() instead.
        """
        import warnings
        warnings.warn('isAlive() is deprecated, use is_alive() instead',
                      DeprecationWarning, stacklevel=2)
        return self.is_alive()

    @property
    def daemon(self):
        """A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when no alive non-daemon threads are
        left.

        """
        assert self._initialized, "Thread.__init__() not called"
        return self._daemonic

    @daemon.setter
    def daemon(self, daemonic):
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if self._started.is_set():
            raise RuntimeError("cannot set daemon status of active thread")
        self._daemonic = daemonic

    def isDaemon(self):
        return self.daemon

    def setDaemon(self, daemonic):
        self.daemon = daemonic

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

# The timer class was contributed by Itamar Shtull-Trauring


'''
暂停对thread的研究了。起码获取了两个信息。start jion

主线程调用Thread实例的start方法:新创建一个线程并返回一个id
这个子线程是这样的Start a new thread and return its identifier. The thread executes the function function
with the argument list args (which must be a tuple). The optional kwargs argument specifies
 a dictionary of keyword arguments. When the function returns, the thread silently exits.
 When the function terminates with an unhandled exception, a stack trace is printed and then
 the thread exits (but other threads continue to run).

子线程去执行这个Thread实例的方法 ---这里有个问题假设主线程调用Thread实例的start的_start_new_thread返
回后在self._bootstrap()->self._bootstrap_inner()中的self._started.set()之前wait才行。不然一直wait了。我看别人完全不care这点

self._bootstrap()->self._bootstrap_inner()->self._set_tstate_lock()获得一个特殊的锁。这个锁是这样的:
special "sentinel" lock that gets released automatically by the interpreter when the thread shuts down

主线程调用Thread实例的join方法:会调用_wait_for_tstate_lock这个方法。这个方法有两个结果。用新线程创建的锁。如果是空了。
说明新线程已经退出了解释器自动释放了。所以抛出异常。即join不了
否则必定acquire不到控制权则阻塞在这直到新线程shutdown。因为就相当于主线程去等待子线程结束就好像两个线程合在了一起所以叫join.你不join线程也会结束的
而且join也就只干了设置标志位而已.而且_is_stopped  _tstate_lock都是这个类实例的。也没对其他线程有影响

如果join给定了时间
When the timeout argument is present and not None, it should be a
floating point number specifying a timeout for the operation in seconds
(or fractions thereof). As join() always returns None, you must call
is_alive() after join() to decide whether a timeout happened -- if the
thread is still alive, the join() call timed out.

官方不建议用daemon因为线程退出的时候可能没有合理释放资源
Daemon threads are abruptly stopped at shutdown. Their resources (such as open files, database transactions, etc.) may
 not be released properly. If you want your threads to stop gracefully, make them non-daemonic and use a suitable
 signalling mechanism such as an Event.
'''

#到目前为止凡是使用条件变量的类都是使用Lock初始化避免了多次释放的麻烦

class Timer(Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=None, kwargs=None):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)  #主线程等待interval时间除非cancel
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)#
        self.finished.set()

    #time.start()方法运行run启动定时器。因为run是在主线程新创建的线程中执行的。
    #所以那个线程会等待interval(因为flag一直是false除非定时器cancel)。然后执行func。执行完然后set设置flag为真。线程执行完了run方法安然退出也没join666


# Special thread class to represent the main thread

#这个是主线程。官网的说法是Return the main Thread object. In normal conditions, the main thread is the thread from which the Python interpreter was started.
class _MainThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="MainThread", daemon=False)
        self._set_tstate_lock()
        self._started.set()
        self._set_ident()
        with _active_limbo_lock:
            _active[self._ident] = self


# Dummy thread class to represent threads not started here.
# These aren't garbage collected when they die, nor can they be waited for.
# If they invoke anything in threading.py that calls current_thread(), they
# leave an entry in the _active dict forever after.
# Their purpose is to return *something* from current_thread().
# They are marked as daemon threads so we won't wait for them
# when we exit (conform previous semantics).

#虚拟线程不值得注意
class _DummyThread(Thread):

    def __init__(self):
        Thread.__init__(self, name=_newname("Dummy-%d"), daemon=True)

        self._started.set()
        self._set_ident()
        with _active_limbo_lock:
            _active[self._ident] = self

    def _stop(self):
        pass

    def is_alive(self):
        assert not self._is_stopped and self._started.is_set()
        return True

    def join(self, timeout=None):
        assert False, "cannot join a dummy thread"


# Global API functions

def current_thread():
    """Return the current Thread object, corresponding to the caller's thread of control.

    If the caller's thread of control was not created through the threading
    module, a dummy thread object with limited functionality is returned.

    """
    try:
        return _active[get_ident()]   #_active = {}    # maps thread id to Thread object
    except KeyError:
        return _DummyThread()

currentThread = current_thread

def active_count():
    """Return the number of Thread objects currently alive.

    The returned count is equal to the length of the list returned by
    enumerate().

    """
    with _active_limbo_lock:
        return len(_active) + len(_limbo)

activeCount = active_count

def _enumerate():
    # Same as enumerate(), but without the lock. Internal use only.
    return list(_active.values()) + list(_limbo.values())

def enumerate():
    """Return a list of all Thread objects currently alive.

    The list includes daemonic threads, dummy thread objects created by
    current_thread(), and the main thread. It excludes terminated threads and
    threads that have not yet been started.

    """
    with _active_limbo_lock:
        return list(_active.values()) + list(_limbo.values())

from _thread import stack_size

# Create the main thread object,
# and make it available for the interpreter
# (Py_Main) as threading._shutdown.

_main_thread = _MainThread()

def _shutdown():
    # Obscure:  other threads may be waiting to join _main_thread.  That's
    # dubious, but some code does it.  We can't wait for C code to release
    # the main thread's tstate_lock - that won't happen until the interpreter
    # is nearly dead.  So we release it here.  Note that just calling _stop()
    # isn't enough:  other threads may already be waiting on _tstate_lock.
    if _main_thread._is_stopped:
        # _shutdown() was already called
        return
    tlock = _main_thread._tstate_lock
    # The main thread isn't finished yet, so its thread state lock can't have
    # been released.
    assert tlock is not None
    assert tlock.locked()
    tlock.release()
    _main_thread._stop()
    t = _pickSomeNonDaemonThread()
    while t:
        t.join()
        t = _pickSomeNonDaemonThread()

def _pickSomeNonDaemonThread():
    for t in enumerate():
        if not t.daemon and t.is_alive():
            return t
    return None

def main_thread():
    """Return the main thread object.

    In normal conditions, the main thread is the thread from which the
    Python interpreter was started.
    """
    return _main_thread

# get thread-local implementation, either from the thread
# module, or from the python fallback

try:
    from _thread import _local as local
except ImportError:
    from _threading_local import local

'''
哇这是个好东西 线程私有的数据
Thread-Local Data¶
Thread-local data is data whose values are thread specific. To manage thread-local data, just create an instance of local (or a subclass) and store attributes on it:

mydata = threading.local()
mydata.x = 1
The instance’s values will be different for separate threads.

class threading.local
A class that represents thread-local data.

For more details and extensive examples, see the documentation string of the _threading_local module.
'''

def _after_fork():
    """
    Cleanup threading module state that should not exist after a fork.
    """
    # Reset _active_limbo_lock, in case we forked while the lock was held
    # by another (non-forked) thread.  http://bugs.python.org/issue874900
    global _active_limbo_lock, _main_thread
    _active_limbo_lock = _allocate_lock()

    # fork() only copied the current thread; clear references to others.
    new_active = {}
    current = current_thread()
    _main_thread = current
    with _active_limbo_lock:
        # Dangling thread instances must still have their locks reset,
        # because someone may join() them.
        threads = set(_enumerate())
        threads.update(_dangling)
        for thread in threads:
            # Any lock/condition variable may be currently locked or in an
            # invalid state, so we reinitialize them.
            if thread is current:
                # There is only one active thread. We reset the ident to
                # its new value since it can have changed.
                thread._reset_internal_locks(True)
                ident = get_ident()
                thread._ident = ident
                new_active[ident] = thread
            else:
                # All the others are already stopped.
                thread._reset_internal_locks(False)
                thread._stop()

        _limbo.clear()
        _active.clear()
        _active.update(new_active)
        assert len(_active) == 1


if hasattr(_os, "register_at_fork"):
    _os.register_at_fork(after_in_child=_after_fork)
