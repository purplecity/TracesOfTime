=【import os
import signal

from . import util

__all__ = ['Popen']

#
# Start child process using fork
#


        # step9
class Popen(object):
    method = 'fork'

    def __init__(self, process_obj):
        util._flush_std_streams()
        #强制刷新缓冲区
        self.returncode = None
        self.finalizer = None  #Finalize实例
        self._launch(process_obj)

    def duplicate_for_child(self, fd):
        return fd

    def poll(self, flag=os.WNOHANG):
        '''
        os.WNOHANG
        The option for waitpid() to return immediately if no child process status is available immediately.
         The function returns (0, 0) in this case. 其实就是放到waitpid中 使父进程不挂起 而立即返回
        '''
        if self.returncode is None:
            try:
                pid, sts = os.waitpid(self.pid, flag)
                '''
                On Unix: Wait for completion of a child process given by process id pid, and return a tuple
                 containing its process id and exit status indication (encoded as for wait()).
                 其实就是linux上的东西 返回子进程pid和状态 如果参数self.pid小于等于0也有不同的含义
                '''
            except OSError as e:
                # Child process not yet created. See #1731717
                # e.errno == errno.ECHILD == 10
                return None
            if pid == self.pid:
                if os.WIFSIGNALED(sts):
                    '''
                    os.WIFSIGNALED(status)
                    Return True if the process exited due to a signal, otherwise return False.
                    '''
                    self.returncode = -os.WTERMSIG(sts)
                    '''
                    os.WTERMSIG(status)
                    Return the signal which caused the process to exit.
                    '''
                else:
                    assert os.WIFEXITED(sts), "Status is {:n}".format(sts)
                    '''
                    os.WIFEXITED(status)
                    Return True if the process exited using the exit(2) system call, otherwise return False.
                    '''
                    self.returncode = os.WEXITSTATUS(sts)
                    '''
                    os.WEXITSTATUS(status)
                    If WIFEXITED(status) is true, return the integer parameter to the exit(2) system call.
                    Otherwise, the return value is meaningless.
                    '''
                #反正这个ifelse就是返回退出码 不是信号终止的就是系统终止的 返回他们的退出码
        return self.returncode

    def wait(self, timeout=None):
        if self.returncode is None:
            if timeout is not None:
                from multiprocessing.connection import wait
                if not wait([self.sentinel], timeout):  #selector 直到sentinel可读 那就是子进程执行完了函数通过pipe告诉父进程
                    return None
            # This shouldn't block if wait() returned successfully.
            return self.poll(os.WNOHANG if timeout == 0.0 else 0) #就是设置退出码
        return self.returncode

    def _send_signal(self, sig):
        if self.returncode is None:
            try:
                os.kill(self.pid, sig)
            except ProcessLookupError:
                pass
            except OSError:
                if self.wait(timeout=0.1) is None:
                    raise

    def terminate(self):
        self._send_signal(signal.SIGTERM)

    def kill(self):
        self._send_signal(signal.SIGKILL)

    # 上面这三个函数就是发送信号
    def _launch(self, process_obj):
        code = 1
        parent_r, child_w = os.pipe()
        #这他吗直接谁父进程读 子进程写的意思？
        '''
        os.pipe()
        Create a pipe. Return a pair of file descriptors (r, w) usable for reading
        and writing, respectively. The new file descriptor is non-inheritable.
        '''

        self.pid = os.fork()
        '''
        os.fork()
        Fork a child process. Return 0 in the child and the
        child’s process id in the parent. If an error occurs OSError is raised.
        '''
        if self.pid == 0:
            try:
                os.close(parent_r)  #意味着子进程 做该做的_bootstrap事情 把父进程的文件描述符关了 fork的话文件描述符是继承了的
                code = process_obj._bootstrap()  #子进程干活
            finally:
                os._exit(code)
        else:
            os.close(child_w) #
            self.finalizer = util.Finalize(self, os.close, (parent_r,))
            self.sentinel = parent_r  #就是一个文件描述符

    def close(self):
        if self.finalizer is not None:
            self.finalizer()
        #卧槽绕来绕去
