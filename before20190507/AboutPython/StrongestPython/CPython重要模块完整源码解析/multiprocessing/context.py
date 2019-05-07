import os
import sys
import threading

from . import process
from . import reduction

__all__ = ()

#
# Exceptions
#

class ProcessError(Exception):
    pass

class BufferTooShort(ProcessError):
    pass

class TimeoutError(ProcessError):
    pass

class AuthenticationError(ProcessError):
    pass

#
# Base type for contexts. Bound methods of an instance of this type are included in __all__ of __init__.py
#

class BaseContext(object):

    ProcessError = ProcessError
    BufferTooShort = BufferTooShort
    TimeoutError = TimeoutError
    AuthenticationError = AuthenticationError

    current_process = staticmethod(process.current_process)
    active_children = staticmethod(process.active_children)
    #  每个方法属性逐一分析 multiprocessing就完事了  跟thrading模块有queue一样 multiprocessing也导入这些
    def cpu_count(self):
        '''Returns the number of CPUs in the system'''
        num = os.cpu_count()
        if num is None:
            raise NotImplementedError('cannot determine number of cpus')
        else:
            return num


# manager mmap实现的sharedctypes  synchronize有啥关系呢  应该是因为有了manager和mmap才有同步这样的操作的
# 官网说法Sharing state between processes分两种
#   Server process
 # A manager object returned by Manager() controls a server process which holds Python objects and allows
 # other processes to manipulate them using proxies.
 # Shared memory  就是 value array这些
 # 总结就是一个是serverproxy 一个 是共享内存当然是可以的
 # 另外就是mmap只有value dict 和arrar list其他类型不支持 manager是采用proxy的方式 支持list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition,
 # Event, Barrier, Queue, Value and Array.

 # 还剩下 manager pool queue  这三个也是核心部分 manager涉及到分布式计算 pool进程池 queue看起来也很6 时间原因以后python用到或者c++需要再来了
    def Manager(self):
        '''Returns a manager associated with a running server process

        The managers methods such as `Lock()`, `Condition()` and `Queue()`
        can be used to create shared objects.
        '''
        from .managers import SyncManager
        m = SyncManager(ctx=self.get_context())
        m.start()
        return m

    def Pipe(self, duplex=True):
        '''Returns two connection object connected by a pipe'''
        from .connection import Pipe
        return Pipe(duplex)

    def Lock(self):
        '''Returns a non-recursive lock object'''
        from .synchronize import Lock
        return Lock(ctx=self.get_context())

    def RLock(self):
        '''Returns a recursive lock object'''
        from .synchronize import RLock
        return RLock(ctx=self.get_context())

    def Condition(self, lock=None):
        '''Returns a condition object'''
        from .synchronize import Condition
        return Condition(lock, ctx=self.get_context())

    def Semaphore(self, value=1):
        '''Returns a semaphore object'''
        from .synchronize import Semaphore
        return Semaphore(value, ctx=self.get_context())

    def BoundedSemaphore(self, value=1):
        '''Returns a bounded semaphore object'''
        from .synchronize import BoundedSemaphore
        return BoundedSemaphore(value, ctx=self.get_context())

    def Event(self):
        '''Returns an event object'''
        from .synchronize import Event
        return Event(ctx=self.get_context())

    def Barrier(self, parties, action=None, timeout=None):
        '''Returns a barrier object'''
        from .synchronize import Barrier
        return Barrier(parties, action, timeout, ctx=self.get_context())

    def Queue(self, maxsize=0):
        '''Returns a queue object'''
        from .queues import Queue
        return Queue(maxsize, ctx=self.get_context())

    def JoinableQueue(self, maxsize=0):
        '''Returns a queue object'''
        from .queues import JoinableQueue
        return JoinableQueue(maxsize, ctx=self.get_context())

    def SimpleQueue(self):
        '''Returns a queue object'''
        from .queues import SimpleQueue
        return SimpleQueue(ctx=self.get_context())

    def Pool(self, processes=None, initializer=None, initargs=(),
             maxtasksperchild=None):
        '''Returns a process pool object'''
        from .pool import Pool
        return Pool(processes, initializer, initargs, maxtasksperchild,
                    context=self.get_context())

    # 接下来的这几个是通过mmap共享内存子进程可以继承来实现的 也可以不看 是安全的因为加了锁
    def RawValue(self, typecode_or_type, *args):
        '''Returns a shared object'''
        from .sharedctypes import RawValue
        return RawValue(typecode_or_type, *args)

    def RawArray(self, typecode_or_type, size_or_initializer):
        '''Returns a shared array'''
        from .sharedctypes import RawArray
        return RawArray(typecode_or_type, size_or_initializer)

    def Value(self, typecode_or_type, *args, lock=True):
        '''Returns a synchronized shared object'''
        from .sharedctypes import Value
        return Value(typecode_or_type, *args, lock=lock,
                     ctx=self.get_context())

    def Array(self, typecode_or_type, size_or_initializer, *, lock=True):
        '''Returns a synchronized shared array'''
        from .sharedctypes import Array
        return Array(typecode_or_type, size_or_initializer, lock=lock,
                     ctx=self.get_context())

    def freeze_support(self):
        '''Check whether this is a fake forked process in a frozen executable.
        If so then run code specified by commandline and exit.
        '''
        if sys.platform == 'win32' and getattr(sys, 'frozen', False):
            from .spawn import freeze_support
            freeze_support()

    def get_logger(self):
        '''Return package logger -- if it does not already exist then
        it is created.
        '''
        from .util import get_logger
        return get_logger()

    def log_to_stderr(self, level=None):
        '''Turn on logging and add a handler which prints to stderr'''
        from .util import log_to_stderr
        return log_to_stderr(level)

    def allow_connection_pickling(self):
        '''Install support for sending connections and sockets
        between processes
        '''
        # This is undocumented.  In previous versions of multiprocessing
        # its only effect was to make socket objects inheritable on Windows.
        from . import connection

    def set_executable(self, executable):
        '''Sets the path to a python.exe or pythonw.exe binary used to run
        child processes instead of sys.executable when using the 'spawn'
        start method.  Useful for people embedding Python.
        '''
        from .spawn import set_executable
        set_executable(executable)

    def set_forkserver_preload(self, module_names):
        '''Set list of module names to try to load in forkserver process.
        This is really just a hint.
        '''
        from .forkserver import set_forkserver_preload
        set_forkserver_preload(module_names)

    def get_context(self, method=None):
        if method is None:
            return self
        try:
            ctx = _concrete_contexts[method]
        except KeyError:
            raise ValueError('cannot find context for %r' % method) from None
        ctx._check_available()
        return ctx

    def get_start_method(self, allow_none=False):
        return self._name

    def set_start_method(self, method, force=False):
        raise ValueError('cannot set start method of concrete context')

    @property
    def reducer(self):
        '''Controls how objects will be reduced to a form that can be
        shared with other processes.'''
        return globals().get('reduction')

    @reducer.setter
    def reducer(self, reduction):
        globals()['reduction'] = reduction

    def _check_available(self):
        pass

#
# Type of default context -- underlying context can be set at most once
#

class Process(process.BaseProcess):
    _start_method = None
    @staticmethod
    def _Popen(process_obj):
        return _default_context.get_context().Process._Popen(process_obj)

class DefaultContext(BaseContext):
    Process = Process
    #step6  就是上面的Process  然后_Popen还是返回默认的的context的Process的_Popen
    #因为在init中是除了_开头的都导入的 所以Process也会导入

    def __init__(self, context):
        self._default_context = context
        self._actual_context = None

    def get_context(self, method=None):
        if method is None:
            if self._actual_context is None:
                self._actual_context = self._default_context
            return self._actual_context
        else:
            return super().get_context(method)
    #step3 返回的是对应名字的context  ForkContext  SpawnContext  ForkServerContext

    def set_start_method(self, method, force=False):
        if self._actual_context is not None and not force:
            raise RuntimeError('context has already been set')
        if method is None and force:
            self._actual_context = None
            return
        self._actual_context = self.get_context(method)
    #step4 这个就是直接使用默认的 DefaultContext 只不过它的属性_actual_context变成了
    #ForkContext  SpawnContext  ForkServerContext 之一



    def get_start_method(self, allow_none=False):
        if self._actual_context is None:
            if allow_none:
                return None
            self._actual_context = self._default_context
        return self._actual_context._name

    def get_all_start_methods(self):
        if sys.platform == 'win32':
            return ['spawn']
        else:
            if reduction.HAVE_SEND_HANDLE:
                return ['fork', 'spawn', 'forkserver']
            else:
                return ['fork', 'spawn']
    #step5 上面这两个函数纯粹是参考信息
    #到此为止的总结 你不初始化就是默认的 要想特定方法就set_stat_method 或者get_context 一般默认的就够了
#
# Context types for fixed start method
#

if sys.platform != 'win32':
    #3个context 3个process
    class ForkProcess(process.BaseProcess):
        _start_method = 'fork'
        @staticmethod
        def _Popen(process_obj):
            from .popen_fork import Popen
            return Popen(process_obj)
    #step8  就是这些创建进程的方式  而BaseProcess又是模仿了threading.Thread的
    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'
        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_posix import Popen
            return Popen(process_obj)

    class ForkServerProcess(process.BaseProcess):
        _start_method = 'forkserver'
        @staticmethod
        def _Popen(process_obj):
            from .popen_forkserver import Popen
            return Popen(process_obj)

    class ForkContext(BaseContext):
        _name = 'fork'
        Process = ForkProcess

    class SpawnContext(BaseContext):
        _name = 'spawn'
        Process = SpawnProcess

    class ForkServerContext(BaseContext):
        _name = 'forkserver'
        Process = ForkServerProcess
        def _check_available(self):
            if not reduction.HAVE_SEND_HANDLE:
                raise ValueError('forkserver start method not available')

    _concrete_contexts = {
        'fork': ForkContext(),
        'spawn': SpawnContext(),
        'forkserver': ForkServerContext(),
    }
    _default_context = DefaultContext(_concrete_contexts['fork'])
    #step2 所以默认就是fork操作的 对于unix来说   重要的是只要导入multiprocessing 就已经实例化DefaultContext这个类了
else:

    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'
        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_win32 import Popen
            return Popen(process_obj)

    class SpawnContext(BaseContext):
        _name = 'spawn'
        Process = SpawnProcess

    _concrete_contexts = {
        'spawn': SpawnContext(),
    }
    _default_context = DefaultContext(_concrete_contexts['spawn'])



#
# Force the start method
#


# step7  到此之前就是导入的是DefaultContext和BaseContext中的除了下划线开头的地方
#使用默认的context或者set_start_method也没问题但是源码上来说就稍微绕一点  倒是挺简单的
#要看的也就是这些导入的东西如何实现的
# 下面这些函数就是 要导入的方法或者属性中用到的
def _force_start_method(method):
    _default_context._actual_context = _concrete_contexts[method]

#
# Check that the current thread is spawning a child process
#

_tls = threading.local()
#线程私有属性 应该是一个mapping

def get_spawning_popen():
    return getattr(_tls, 'spawning_popen', None)

def set_spawning_popen(popen):
    _tls.spawning_popen = popen

def assert_spawning(obj):
    if get_spawning_popen() is None:
        raise RuntimeError(
            '%s objects should only be shared between processes'
            ' through inheritance' % type(obj).__name__
            )
