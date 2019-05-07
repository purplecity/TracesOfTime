# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 7:28 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_22.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 定义上下文管理器的简单方法

# @contextmanager 应该仅仅用来写自包含的上下文管理函数。 如果你有一些对象(比如一个文件、网络连接或锁)，需要支持 with 语句，那么你就需要单独实现 __enter__() 方法和 __exit__() 方法。

import time
from contextlib import contextmanager

@contextmanager
def timethid(label):
    start=time.time()
    try: yield
    finally:
        end = time.time()
        print('{}:{}'.format(label,end-start))

with timethid('counting'):
    n=10000
    while n>0: n -= 1

    #当所有代码运行完成并且不出现异常的情况下才会生效?

'''
def contextmanager(func):
    """@contextmanager decorator.

    Typical usage:

        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        with some_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>
'''
