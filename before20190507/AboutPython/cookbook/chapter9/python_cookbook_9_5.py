# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/16 7:34 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_5.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#不由得感叹之前我的专题解决很有效。现在进度很快。
# 可自定义属性的装饰器
# 你想写一个装饰器来包装一个函数，并且允许用户提供参数在运行时控制装饰器行为。


from functools import wraps,partial
import logging
import time

def attach_wrapper(obj,func=None):
    if func is None:
        return partial(attach_wrapper,obj)
    setattr(obj,func.__name__,func)
    return func

def logged(level,name=None,message=None):
    def decorate(func):
        logname=name if name else func.__module__
        log=logging.getLogger(logname)
        logmsg=message if message else func.__name__

        @wraps(func)
        def wrapper(*args,**kwargs):
            log.log(level,logmsg)
            return func(*args,**kwargs)

        @attach_wrapper(wrapper)  #wrapper=wraps(func)(wrapper)  已经更改了是一个obj
        def set_level(newlevel):
            nonlocal  level  #声明不是闭包的局部变量是外函数的变量。用来更改外函数变量的
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal  logmsg
            logmsg=newmsg

        return wrapper

    return decorate

@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL)
def spam():
    print('Spam!')

'''
logging.basicConfig(level=logging.DEBUG)
print(add(2,3))

add.set_message('add called')  # add已经是一个函数obj(function object)。居然可以再用.号调用内部属性。意犹未尽
print(add(2,3))

add.set_level(logging.WARNING)  #WARNING:__main__:add called
print(add(2,3))
#5
#DEBUG:__main__:add called
'''
#这一小节的关键点在于访问函数(如 set_message() 和 set_level() )，它们被作为属性赋给包装器。 每个访问函数允许使用 nonlocal 来修改函数内部的变量。


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return 3  #countdown这个函数没有return所以这个是None
    return wrapper

@timethis
@logged(logging.DEBUG)
def countdown(n):
    while n > 0:
        n -= 1
    return 2

a=countdown(10000)
print(a)  #尽管两个装饰器返回的值不同。但是打印的是最外层装饰器的返回值  这可能跟多个装饰器的转化有关
'''
DEBUG:__main__:countdown
countdown 0.0006158351898193359
'''

#  使用set_level和set_message跟 timethis 和logged的顺序没关系 这是需要注意的。