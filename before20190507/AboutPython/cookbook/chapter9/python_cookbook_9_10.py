# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/17 9:53 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_10.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 上一章把装饰器做成一个类。是有call方法的。当被装饰的函数或者类有实参的时候就调用call？


#给类方法或者静态方法提供装饰器  确保装饰器在 @classmethod 或 @staticmethod 之前

import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        r=func(*args,**kwargs)
        end=time.time()
        print(end-start)
        return r
    return wrapper


class Spam:
    @timethis
    def instance_method(self,n):
        print(self,n)
        while n>0: n -= 1

    @classmethod
    @timethis
    def class_method(cls,n):
        print(cls,n)
        while n>0: n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0: n -= 1


s=Spam()
s.instance_method(1000)
Spam.class_method(1000)
Spam.static_method(10000)

'''

class Spam:
    @timethis
    @staticmethod
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1
            
            
>>> Spam.static_method(1000000)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "timethis.py", line 6, in wrapper
start = time.time()
TypeError: 'staticmethod' object is not callable
>>>

问题在于 @classmethod 和 @staticmethod 实际上并不会创建可直接调用的对象， 而是创建特殊的描述器对象(参考8.9小节)。因此当你试着在其他装饰器中将它们当做函数来使用时就会出错。

毕竟timethis接收的是一个可以调用的函数。
'''