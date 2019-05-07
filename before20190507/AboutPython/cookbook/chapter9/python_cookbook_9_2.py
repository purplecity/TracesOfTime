# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/16 6:57 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_2.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import time
from functools import wraps
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
        return result
    return wrapper

@timethis
def countdown(n):
    while n>0:
        n -= 1

print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)
print(countdown.__wrapped__(10000))
from inspect import signature
print(signature(countdown))