# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/16 7:13 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_4.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

from functools import wraps
import logging

def logged(level,name=None,message=None):

    def decorate(func):
        logname=name if name else func.__module__
        print(func.__module__)
        log=logging.getLogger(logname)
        logmsg=message if message else func.__name__
        print(func.__name__)

        @wraps(func)
        def wrapper(*args,**kwargs):
            log.log(level,logmsg)
            return func(*args,**kwargs)
        return wrapper #这个是包装器  包装器可以使用传递给logged的参数
    return decorate  #这个是装饰器函数


@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, message='example')
def spam():
    print('Spam!')

'''

__main__
add
__main__
spam
'''