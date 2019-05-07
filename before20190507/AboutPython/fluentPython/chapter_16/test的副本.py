
'''
class DemoException(Exception):
    ''''''


def demo_exec_handling():
    print("-> coroutine started")
    while True:
        try:
            x = yield  1
        except DemoException:
            print("****DemoException handled***")
        else:
            print("-> coroutine received:{!r}".format(x))
    raise RuntimeError("this line should never run")


exec_coro = demo_exec_handling()
next(exec_coro)
exec_coro.send(11)
a = exec_coro.throw(DemoException)
print(a)
from inspect import getgeneratorstate

print(getgeneratorstate(exec_coro))


from collections import namedtuple

Result = namedtuple("Result","count average")

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count

    return Result(count,average)
















data = {
    "girls;kg":[10.1,10.2,10.3,10.4,10.5,10.6,10.7],
    "girls;m":[11.1,11.2,11.3,11.4,11.5,11.6,11.7],
    "boys;kg":[12.1,12.2,12.3,12.4,12.5,12.6,12.7],
    "boys;m":[13.1,13.2,13.3,13.4,13.5,13.6,13.7]
}

from collections import namedtuple

Result = namedtuple("result","count average")

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        if term is None:
            break
        total += term
        count += 1
        average = total/count

    return Result(count,average)

def grouper(results,key):
    while True:
        results[key] = yield from averager()
        print(results[key])

def main(data):
    results = {}
    for key,values in data.items():
        group = grouper(results,key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    report(results)


def report(results):

    for key,result in sorted(results.items()):
        group,unit = key.split(";")

        print("{:2} {:5} averaging {:.2f}{}".format(result.count,group,result.average,unit))


main(data)
'''




''' 单纯的send yield
def simplle(a):
    print("start-> a=",a)
    b = yield a
    #yield a
    print("receive-> b=",b)
    c = yield a+b
    print("received :c=",c)

#send的作用就是使生成器从当前yield暂停处前进到下一个yield处暂停，下一个yield的产出值是send的返回值。 send的发送的值会成为当前yield暂停处的表达式的值。启动就是发送None值，使生成器启动到第一个yield语句处暂停

x =simplle(5)
m1 = x.send(None) #
m2=x.send(10)

'''

# yield from 的主要功能是打开双向通道。把最外曾的调用方和最内层的子生成器连接起来，这样二者可以直接发送和产出值。
# RESULT=yield from EXPR的简洁精简操作

'''
_i = iter(EXPR)

try:
    _y = next(_i)
    # 子生成器第一次yield产出_y
except StopIteration as _e:
    _r = _e.value
else:
    while 1:
        # 委派生成器会阻塞在下一行的yield处。 等到调用方发送send
        _s = yield _y #调用方第一次拿到的值就是_y.然后再次send的值保存在_s中。返回值是上一次的y经过下面操作之后再到此yield
        
        try:
            _y = _i.send(_s) #发送的值会直接发送给子生成器让子生成器yield产出值给_y
        except StopIteration as _e:
            _r = _e.value
            break

RESULT = _r



'''

#与书上相比我在averager函数中yield 了 average。然后send后面添加了返回值。更加清楚了。但是结果告诉我们浮点数运算千万要小心。真的。
data = {
    "girls;kg":[10.1,10.2,10.3,10.4,10.5,10.6,10.7],
    "girls;m":[11.1,11.2,11.3,11.4,11.5,11.6,11.7],
    "boys;kg":[12.1,12.2,12.3,12.4,12.5,12.6,12.7],
    "boys;m":[13.1,13.2,13.3,13.4,13.5,13.6,13.7]
}

from collections import namedtuple

Result = namedtuple("result","count average")

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        if term is None:
            break
        total += term
        count += 1
        average = total/count

    return Result(count,average)

def grouper(results,key):
    while True:
        results[key] = yield from averager()
        #print(results[key])

def main(data):
    results = {}
    for key,values in data.items():
        group = grouper(results,key)
        next(group)
        for value in values:
            test = group.send(value)
            print(test)
        group.send(None)
    report(results)


def report(results):

    for key,result in sorted(results.items()):
        group,unit = key.split(";")

        print("{:2} {:5} averaging {:.2f}{}".format(result.count,group,result.average,unit))


main(data)

# 第一遍值得品味，那个出租车仿真。


