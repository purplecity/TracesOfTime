# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/21 12:46 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_14_1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# python提供了测试模块 unittest。算了暂时不看 跟resource 控制内存和cpu一样。临时所需。平时所需不大
# 14.6   except可以接受异常类组成的元组
# 14.7 Exception除了System，keyboardInterrupt GeneratorExit之外所有的异常
# 捕获所有的异常的异常BaseException
# 14.8 创建自定义异常

'''
自定义异常类应该总是继承自内置的 Exception 类， 或者是继承自那些本身就是从 Exception 继承而来的类。 尽管所有类同时也继承自 BaseException ，但你不应该使用这个基类来定义新的异常。 BaseException 是为系统退出异常而保留的，比如 KeyboardInterrupt 或 SystemExit 以及其他那些会给应用发送信号而退出的异常。 因此，捕获这些异常本身没什么意义。 这样的话，假如你继承 BaseException 可能会导致你的自定义异常不会被捕获而直接发送信号退出程序运行。c
.args 其实就是init的参数可以随便多少个参数和字段
'''
#14.09 捕获异常后抛出另外的异常  同时保留两个异常信息的话 raise from e( except error类 as e)  看来抛出另外一个异常的话最好raise from
# 14.10重新抛出被捕获的异常   你需要在捕获异常后执行某个操作（比如记录日志、清理等），但是之后想将异常传播下去
# 14.11  输出警告信息 在你维护软件，提示用户某些信息，但是又不需要将其上升为异常级别，那么输出警告信息就会很有用了
# import warnings   warnings.warn(警告字符串信息或者警告类)  -W 选项能控制警告消息的输出。 -W all 会输出所有警告消息，-W ignore 忽略掉所有警告，-W error 将警告转换成异常。 另外一种选择，你还可以使用 warnings.simplefilter() 函数控制输出。 always 参数会让所有警告消息出现，`ignore 忽略调所有的警告，error 将警告转换成异常

# 14.12  调试。跟gdb相对的pdb
# 14.13 给程序做性能测试  一般没什么必要。虽然可以直接time python3 **.py
# 函数性能装饰器

import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.perf_counter()
        r=func(*args,**kwargs)
        end=time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

# 代码块运行时间

from contextlib import contextmanager

@contextmanager
def timeblock(label):
    start=time.perf_counter()
    try:
        yield
    finally:
        end=time.perf_counter()
        print('{} : {}'.format(label, end - start))


with timeblock("counting"):
    n=10000
    while n>0:
        n -= 1


# 测试很小的代码块

from timeit import timeit
timeit("math.sqrt(2)","import math",number=10000)

# 关于程序优化的第一个准则是“不要优化”，第二个准则是“不要优化那些无关紧要的部分”。
# 值得看。使用函数。局部变量比全局变量要快的多


# 使用内置的容器
#
# 内置的数据类型比如字符串、元组、列表、集合和字典都是使用C来实现的，运行起来非常快。 如果你想自己实现新的数据结构（比如链接列表、平衡树等）， 那么要想在性能上达到内置的速度几乎不可能，因此，还是乖乖的使用内置的吧。


'''
a = {
    'name' : 'AAPL',
    'shares' : 100,
    'price' : 534.22
}

b = dict(name='AAPL', shares=100, price=534.22)
'''