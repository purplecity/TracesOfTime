
# ------------------------------------------------线程------------------------------------------------------------------

# Copyright 2009 Brian Quinlan. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Implements ThreadPoolExecutor."""

__author__ = 'Brian Quinlan (brian@sweetapp.com)'

import atexit
from concurrent.futures import _base
import itertools
import queue
import threading
import weakref
import os

# Workers are created as daemon threads. This is done to allow the interpreter
# to exit when there are still idle threads in a ThreadPoolExecutor's thread
# pool (i.e. shutdown() was not called). However, allowing workers to die with
# the interpreter has two undesirable properties:
#   - The workers would still be running during interpreter shutdown,
#     meaning that they would fail in unpredictable ways.
#   - The workers could be killed while evaluating a work item, which could
#     be bad if the callable being evaluated has external side-effects e.g.
#     writing to a file.
#
# To work around this problem, an exit handler is installed which tells the
# workers to exit when their work queues are empty and then waits until the
# threads finish.

_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False

def _python_exit():
    global _shutdown
    _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(None)   #ThreadPoolExecutor实例的队列都put一个None。也行吧。None就None。有多少线程就put多少个None.PUT的默认参数block是阻塞的。所以要分两次for循环
    for t, q in items:
        t.join()  #实例的线程都回收

atexit.register(_python_exit)  #把_python_exit注册成正常退出时执行的函数

'''

    thread t ----> work_queue(include   _workItem's instance )
        |
        |
        |
    doing: _work
'''

class _WorkItem(object):
    '''
    purplecity
    workitem: init and run. run-> get result or except
    '''
    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException as exc:
            self.future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None    #清空workitem实例的的其他引用。如果不清空的话ThreadPoolExecutor实例的work_queue中有这个workitem类实例的引用。这个workitem实例在ThreadPoolExecutor实例生命周期中永远不会被回收。除非像这样显示删除其他引用。  同理推导类中有实例的强引用，而类存在的时间与
#Python 进程一样长，除非显式删除类，不然类中实例永远不会被回收
        else:
            self.future.set_result(result)


def _worker(executor_reference, work_queue, initializer, initargs):
    if initializer is not None:
        try:
            initializer(*initargs)  #初始化操作
        except BaseException:
            _base.LOGGER.critical('Exception in initializer:', exc_info=True)
            executor = executor_reference() #返回ThreadPoolExecutor实例的弱引用。
            if executor is not None:  #ThreadPoolExecutor实例还存在
                executor._initializer_failed() #把ThreadPoolExecutor实例中work queue中workitem一个个的都拿出来。然后把对应的future设置为BrokenThreadPool
            return
    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run()  #正常运行
                # Delete references to object. See issue16284
                del work_item # 删除本身实例。毕竟get是remove操作的。所以除了返回ThreadPoolExecutor实例中队列外没有其他引用了
                continue

            # 已经取完了
            executor = executor_reference()
            # Exit if:
            #   - The interpreter is shutting down OR  解释器停了
            #   - The executor that owns the worker has been collected OR 弱引用指向的ThreadPoolExecutor实例不存在了
            #   - The executor that owns the worker has been shutdown.
            if _shutdown or executor is None or executor._shutdown:
                # Flag the executor as shutting down as early as possible if it
                # is not gc-ed yet.
                if executor is not None:
                    executor._shutdown = True  #如果挂掉了就put None shutdown 为true
                # Notice other workers
                work_queue.put(None)
                return
            del executor  #事情搞完就删除这个弱引用对象
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)


class BrokenThreadPool(_base.BrokenExecutor):
    """
    Raised when a worker thread in a ThreadPoolExecutor failed initializing.
    """


class ThreadPoolExecutor(_base.Executor):

    # Used to assign unique thread names when thread_name_prefix is not supplied.
    _counter = itertools.count().__next__

    '''
    purplecity
    def count(start=0, step=1):
    # count(10) --> 10 11 12 13 14 ...
    # count(2.5, 0.5) -> 2.5 3.0 3.5 ...
    n = start
    while True:
        yield n
        n += step

    所以itertools.count()返回一个生成器。 再加个__next__就相当于获得这个生成器的__next__函数对象。然后_counter()就相当于调用这个__next__ 函数即__next__().
    next(生成器)  == 生成器.__next__()
    '''

    def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):
        """Initializes a new ThreadPoolExecutor instance.
        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: An callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        """
        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        if initializer is not None and not callable(initializer):
            raise TypeError("initializer must be a callable")

        self._max_workers = max_workers
        self._work_queue = queue.SimpleQueue()
        self._threads = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))  #purplecity:or 就避免了if else了
        self._initializer = initializer
        self._initargs = initargs

    def submit(self, fn, *args, **kwargs):
        #purplecity:fn, to be executed as fn(*args **kwargs)
        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _shutdown:
                raise RuntimeError('cannot schedule new futures after '
                                   'interpreter shutdown')

            f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)

            self._work_queue.put(w)
            self._adjust_thread_count()
            return f
    submit.__doc__ = _base.Executor.submit.__doc__

    def _adjust_thread_count(self):
        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)
        # TODO(bquinlan): Should avoid creating new threads if there are more
        # idle threads than items in the work queue.
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
            t = threading.Thread(name=thread_name, target=_worker,
                                 args=(weakref.ref(self, weakref_cb),
                                       self._work_queue,
                                       self._initializer,
                                       self._initargs)) #arg参数是传给target的  当self实例即将被删除时候调用weakref_cb函数。传给weakref_cb参数的是self实例的引用。


            t.daemon = True
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    '''
    purplecity
    daemon
    A boolean value indicating whether this thread is a daemon thread (True) or not (False). This must be set before start() is called, otherwise
    RuntimeError is raised. Its initial value is inherited from the creating thread; the
    main thread is not a daemon thread and therefore all threads created in the main thread default to daemon = False.
    The entire Python program exits when no alive non-daemon threads are left.



    '''

    def _initializer_failed(self):
        #purplecity: 如果初始化失败。那么线程池就不能再用了。把work queue中workitem一个个的都拿出来。然后把对应的future设置为BrokenThreadPool
        with self._shutdown_lock:
            self._broken = ('A thread initializer failed, the thread pool '
                            'is not usable anymore')
            # Drain work queue and mark pending futures failed
            while True:
                try:
                    work_item = self._work_queue.get_nowait()

                    '''
                    purplecity： simpleQueue也是一种FIFO队列
                    SimpleQueue.get(block=True, timeout=None)
                    Remove and return an item from the queue. If optional args block is true and timeout is None (the default), block
                    if necessary until an item is available. If timeout is a positive number, it blocks at most timeout seconds and raises
                     the Empty exception if no item was available within that time. Otherwise (block is false), return an item if one is
                     immediately available, else raise the Empty exception (timeout is ignored in that case). 如果block为false立即返回一个可用的对象。
                     然false。block为true就一直等待知道一个对象可用或者一定tiemout。 但是这里的avaiable又是啥意思呢

                    SimpleQueue.get_nowait()
                    Equivalent to get(False).

                    '''
                except queue.Empty:
                    break
                if work_item is not None:
                    work_item.future.set_exception(BrokenThreadPool(self._broken))

    def shutdown(self, wait=True):
        # purplecity 获得锁的情况下。把shutdown标志为true。并网workitem Queue中发送一个None。如果wait为true就阻塞回收当前所有的线程
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(None)  #None也是一个元素。占长度的。返回是None.
        if wait:
            for t in self._threads:
                t.join()
    shutdown.__doc__ = _base.Executor.shutdown.__doc__



# 线程总结。ThreadPoolExecutor有两个操作。 shutdown 和  submit。 shutdown就是把自身_shutdown设置为true表示要关了。然后_work_queue put一个None。 把当前线程都回收(默认就是true。不回收你也不能用这些线程了)。
# 如果del ThreadPoolExecutor实例。直接del 不先shutdown的话每个线程还是会put None。重点是submit。每调用一次summit,就会创建一个线程。但是有2个不行的。就是不能多于max线程数否则不会创建线程。也没有避免创建多的线程
# 每submit一次。创建一个future对象，一个workitem对象，一个线程，一个弱引用对象，执行一次_work。按照先进先出_work get也是最近的。如果执行ok  删除弱引用，把future设置为完成。
# future是跟func一起的---根据func的结果设置结果。_
