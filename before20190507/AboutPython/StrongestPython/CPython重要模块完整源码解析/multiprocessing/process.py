#
# Module providing the `Process` class which emulates `threading.Thread`
#  这一点很重要  procssing设计的跟thread一样
# multiprocessing/process.py
#
# Copyright (c) 2006-2008, R Oudkerk
# Licensed to PSF under a Contributor Agreement.
#

__all__ = ['BaseProcess', 'current_process', 'active_children']

#
# Imports
#

import os
import sys
import signal
import itertools
import threading
from _weakrefset import WeakSet

#
#
#



try:
    ORIGINAL_DIR = os.path.abspath(os.getcwd())
    #当前文件的绝对路径
except OSError:
    ORIGINAL_DIR = None

#
# Public functions
#

def current_process():
    '''
    Return process object representing the current process
    '''
    return _current_process  #返回_MainProcess实例

def active_children():
    '''
    Return list of process objects corresponding to live child processes
    '''
    _cleanup()
    return list(_children)

#
#
#

def _cleanup():
    # check for processes which have finished
    for p in list(_children):
        if p._popen.poll() is not None:
            _children.discard(p)  #集合的discard就是从集合中删除这个元素  删除后并没有创建新set内存地址并没有变
            '''
            a =set([1,3,5])
            print(a,id(a))
            a.discard(1)
            print(a,id(a))
            '''

#
# The `Process` class
#

class BaseProcess(object):
    '''
    Process objects represent activity that is run in a separate process

    The class is analogous to `threading.Thread`
    跟threading.Thread一样的
    '''
    def _Popen(self):
        raise NotImplementedError

    '''
            def _Popen(process_obj):
                from .popen_fork import Popen
                return Popen(process_obj)

            def _Popen(process_obj):
                from .popen_forkserver import Popen
                return Popen(process_obj)
    '''
    # step9  ok 到现在为止 ForkContext  SpawnContext  ForkServerContext
    #拥有像thrading.Thread一样的process 就是不同popen的BaseProcess 以及 像thrading中的Queue Lock那些一样拥有Queue Lock
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={},
                 *, daemon=None):
        assert group is None, 'group argument must be None for now'
        count = next(_process_counter)
        self._identity = _current_process._identity + (count,)  #进程标识tuple  (1,2,3)
        #基类用子类的实例 ？？？
        self._config = _current_process._config.copy()  #只是一个mapping
        self._parent_pid = os.getpid()
        self._popen = None
        self._closed = False
        self._target = target
        self._args = tuple(args)
        self._kwargs = dict(kwargs)
        self._name = name or type(self).__name__ + '-' + \
                     ':'.join(str(i) for i in self._identity)
        if daemon is not None:
            self.daemon = daemon
        _dangling.add(self)  #保存这实例的弱引用

    def _check_closed(self):
        if self._closed:
            raise ValueError("process object is closed")

    def run(self):
        '''
        Method to be run in sub-process; can be overridden in sub-class
        '''
        if self._target:
            self._target(*self._args, **self._kwargs)

    def start(self):
        '''
        Start child process
        '''
        self._check_closed()
        assert self._popen is None, 'cannot start a process twice'
        assert self._parent_pid == os.getpid(), \
               'can only start a process object created by current process'
        assert not _current_process._config.get('daemon'), \
               'daemonic processes are not allowed to have children'
        _cleanup()
        self._popen = self._Popen(self)
        self._sentinel = self._popen.sentinel
        #step11  还记得吗 线程创建也是用sentinel的
        # Avoid a refcycle if the target function holds an indirect
        # reference to the process object (see bpo-30775)
        del self._target, self._args, self._kwargs
        # 如果目标函数持有对流程对象的间接引用，则避免refcycle(参见bpo-30775)
        _children.add(self) #启动一个就添加到_childred中

    '''
    start run _bootstrap跟threading.Thread一样的 在线程中是 直接
    threading.Thread(target=,args=,kwargs=) 然后start join
    或者直接继承Thread类然后重写run方法
    不管怎样在Thread类中的逻辑是start会调用_bootstrap然后调用run方法 start才是重点
    Thread类中是创建一个线程然后执行完target就安然退出 join只是一个关于锁的操作 并不是去结束子线程
    因为在主线程中调用join  其实就是等待子线程安然退出c语言释放_tstate_lock锁的控制权然后主线程就可以获得_tstate_lock锁控制权
    其实就一个阻塞的过程阻塞子线程target执行完成而已  多个线程都不join都没关系的都是因为一个线程对应这一个实例锁都是实例中的属性
    process也有两种方式跟Thread一样的一种是直接process(target=,args=,kwargs=) 然后start join 因为start会实例话popen 然后调用_launch
    然后调用_bootstrap 然后调用run
    另外也是继承然后重写run  一个进程对应一个process实例也就是 process是单独拿出来用的 queue那些是context中的属性
    卧槽不是吧 难道process也是执行完target后安然退出？应该是

    这里有个关键点 c中fork 然后父子进程通过pipe进行通信 然后父子进程各自关闭pipe创建出的读写文件描述符的其中一个
    那么等子进程完事了 通过pipe告诉父进程完事 python也是一样的所以这里的join就是等待父进程的描述符可读
    注意这里说的pipe是c中的pipe是单向的 而connection中的pipe是 socketpair优化后的双向

    到此为止 context process popen_fork 完结
    multiprocessing有process 和 Queue Lock 跟thread一样的用法 但是还多了pool
    拥有像thrading.Thread一样的process 就是不同popen的BaseProcess 以及 像thrading中的Queue Lock那些一样拥有Queue Lock

    multiprocess用到c++ c还会来此
    thread没有 pool  交换数据只有queue没有pipe  没有共享数据的manager
    同步所有的thread和multiprocess都有


    有必要看官方文档中的Programming guidelines  比如Joining processes that use queues 意思就是进程join之前不要再使用queue了否则死锁

    因为大部分涉及到linux的东西 过一下了解下流程 不用深扣细节  以后迟早回来的
    '''

    def terminate(self):
        '''
        Terminate process; sends SIGTERM signal or uses TerminateProcess()
        '''
        self._check_closed()
        self._popen.terminate()

    def kill(self):
        '''
        Terminate process; sends SIGKILL signal or uses TerminateProcess()
        '''
        self._check_closed()
        self._popen.kill()

    def join(self, timeout=None):
        '''
        Wait until child process terminates
        '''
        self._check_closed()
        assert self._parent_pid == os.getpid(), 'can only join a child process'
        assert self._popen is not None, 'can only join a started process'
        res = self._popen.wait(timeout)
        if res is not None:
            _children.discard(self)

    def is_alive(self):
        '''
        Return whether process is alive
        '''
        self._check_closed()
        if self is _current_process:
            return True
        assert self._parent_pid == os.getpid(), 'can only test a child process'

        if self._popen is None:
            return False

        returncode = self._popen.poll()
        if returncode is None:
            return True
        else:
            _children.discard(self)
            return False

    def close(self):
        '''
        Close the Process object.

        This method releases resources held by the Process object.  It is
        an error to call this method if the child process is still running.
        '''
        if self._popen is not None:
            if self._popen.poll() is None:
                raise ValueError("Cannot close a process while it is still running. "
                                 "You should first call join() or terminate().")
            self._popen.close()
            self._popen = None
            del self._sentinel
            _children.discard(self)
        self._closed = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, str), 'name must be a string'
        self._name = name

    @property
    def daemon(self):
        '''
        Return whether process is a daemon
        '''
        return self._config.get('daemon', False)

    @daemon.setter
    def daemon(self, daemonic):
        '''
        Set whether process is a daemon
        '''
        assert self._popen is None, 'process has already started'
        self._config['daemon'] = daemonic

    @property
    def authkey(self):
        return self._config['authkey']

    @authkey.setter
    def authkey(self, authkey):
        '''
        Set authorization key of process
        '''
        self._config['authkey'] = AuthenticationString(authkey)

    @property
    def exitcode(self):
        '''
        Return exit code of process or `None` if it has yet to stop
        '''
        self._check_closed()
        if self._popen is None:
            return self._popen
        return self._popen.poll()

    @property
    def ident(self):
        '''
        Return identifier (PID) of process or `None` if it has yet to start
        '''
        self._check_closed()
        if self is _current_process:
            return os.getpid()
        else:
            return self._popen and self._popen.pid

    pid = ident

    @property
    def sentinel(self):
        '''
        Return a file descriptor (Unix) or handle (Windows) suitable for
        waiting for process termination.
        '''
        self._check_closed()
        try:
            return self._sentinel
        except AttributeError:
            raise ValueError("process not started") from None

    def __repr__(self):
        exitcode = None
        if self is _current_process:
            status = 'started'
        elif self._closed:
            status = 'closed'
        elif self._parent_pid != os.getpid():
            status = 'unknown'
        elif self._popen is None:
            status = 'initial'
        else:
            exitcode = self._popen.poll()
            if exitcode is not None:
                status = 'stopped'
            else:
                status = 'started'

        info = [type(self).__name__, 'name=%r' % self._name]
        if self._popen is not None:
            info.append('pid=%s' % self._popen.pid)
        info.append('parent=%s' % self._parent_pid)
        info.append(status)
        if exitcode is not None:
            exitcode = _exitcode_to_name.get(exitcode, exitcode)
            info.append('exitcode=%s' % exitcode)
        if self.daemon:
            info.append('daemon')
        return '<%s>' % ' '.join(info)

    ##

    def _bootstrap(self):
        from . import util, context
        global _current_process, _process_counter, _children

        try:
            if self._start_method is not None:
                context._force_start_method(self._start_method)·
            #真尼玛神奇！！！  这是故意的 只有在那三个process继承中才有_start_method这个字段
            _process_counter = itertools.count(1)
            _children = set()
            util._close_stdin()  #其实就是把标准输入重置为dev/null 没有输入
            old_process = _current_process
            _current_process = self
            #尼玛这样赋值的吗
            try:
                util._finalizer_registry.clear() #清空dict
                util._run_after_forkers()  #弱引用字典中逐个执行
            finally:
                # delay finalization of the old process object until after
                # _run_after_forkers() is executed
                del old_process
            util.info('child process calling self.run()')
            try:
                self.run()
                exitcode = 0
            finally:
                util._exit_function()
        except SystemExit as e:
            if not e.args:
                exitcode = 1
            elif isinstance(e.args[0], int):
                exitcode = e.args[0]
            else:
                sys.stderr.write(str(e.args[0]) + '\n')
                exitcode = 1
        except:
            exitcode = 1
            import traceback
            sys.stderr.write('Process %s:\n' % self.name)
            traceback.print_exc()
        finally:
            threading._shutdown()
            #尼玛进程退出 然后还要把对应的线程退出
            util.info('process exiting with exitcode %d' % exitcode)
            util._flush_std_streams()

        return exitcode

#
# We subclass bytes to avoid accidental transmission of auth keys over network
#

class AuthenticationString(bytes):
    def __reduce__(self):
        from .context import get_spawning_popen
        if get_spawning_popen() is None:
            raise TypeError(
                'Pickling an AuthenticationString object is '
                'disallowed for security reasons'
                )
        return AuthenticationString, (bytes(self),)

#
# Create object representing the main process
#

class _MainProcess(BaseProcess):

    def __init__(self):
        self._identity = ()
        self._name = 'MainProcess'
        self._parent_pid = None
        self._popen = None
        self._closed = False
        self._config = {'authkey': AuthenticationString(os.urandom(32)),
                        'semprefix': '/mp'}
        # Note that some versions of FreeBSD only allow named
        # semaphores to have names of up to 14 characters.  Therefore
        # we choose a short prefix.
        #
        # On MacOSX in a sandbox it may be necessary to use a
        # different prefix -- see #19478.
        #
        # Everything in self._config will be inherited by descendant
        # processes. 意思是config都会被子进程继承 就是一个map

    def close(self):
        pass


_current_process = _MainProcess()   #就是一个类实例
_process_counter = itertools.count(1)
'''
_process_counter生成器对象
itertools.count(start=0,step=1)

def count(start=0,step=1):
    n  = start
    while True:
        yield n
        n += step
'''
_children = set()  #只是一个集合
del _MainProcess  #把类删除我草  之前就实例化一个_current_process

#
# Give names to some return codes
#

_exitcode_to_name = {}

for name, signum in list(signal.__dict__.items()):
    if name[:3]=='SIG' and '_' not in name:
        _exitcode_to_name[-signum] = f'-{name}'
        #反向排列退出码
        #尼玛get了新的字符串格式化方法fstring Python3.6引入的


# For debug and leak testing
# 注意这句
_dangling = WeakSet()
