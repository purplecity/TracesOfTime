# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/1 4:07 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_7_11.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 这个联合 https://blog.csdn.net/soonfly/article/details/78361819这个看更有意义

from queue import Queue
from functools import wraps

def add(x,y): return x+y

def apply_async(func,args,*,callback):
    result=func(*args)
    callback(result)

class Async:
    def __init__(self,func,args):
        self.func=func
        self.args=args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper


@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print('is 1',r)
    r = yield Async(add, ('hello', 'world'))
    print('is 2',r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')

test()

#问题的关键是r这个用来接收send发送的函数，是一个假想函数。还是按照他们来。