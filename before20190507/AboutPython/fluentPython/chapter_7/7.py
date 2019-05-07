# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/28 5:44 PM                               
#  Author           purplecity                                       
#  Name             7.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

'''
def deco(func):
    def inner():
        print("running inner()")
    return inner

@deco
def target():
    print("running target()")

target()
print(target)


#装饰器的一大特性是，能把被装饰的函数替换成其他函数。第二个特性是，装饰器在加载模块时立即执行(函数装饰器在导入模块时立即执行import或者main，而被装饰的
#函数只在明确调用时运行。这突出了 Python 程序员所说的导入时和运行时之间的区别)

registry = []
def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func
@register
def f1():
    print('running f1()')
@register
def f2():
    print('running f2()')
def f3():
    print('running f3()')
def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()
if __name__=='__main__':
    main()



def make_average():
    series=[]
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager

avg = make_average()
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)
print(avg(10))
print(avg(11))
print(avg(12))
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)


# co_varnames	tuple of names of arguments and local variables  co_freevars	tuple of names of free variables (referenced via a function’s closure)
#其实，闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系，关键是它能访问定义体之外定义的非全局变量
#意思就是闭包中的内部函数对象保存着自己的局部变量和自由变量。自由变量对于外部函数来说是一个局部变量。保存在对象的__closuere__属性中。对象的__closure__是一个列表
#每个元素对应于对象的__code__.co_freevars的一个名称。这些元素是 cell 对象，有个 cell_contents 属性，保存着真正的值。 那闭包的作用是保存外部函数的局部变量(对于内部函数来说是自由变量)的一份拷贝？
#p317很精彩  数字字符创或者元组等不可变对象的+=会隐式的创建局部变量。只能读取，不能更新，而listdict等可变对象则不会。Python 3 引入了 nonlocal 声明。它的作用是把变
#量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量。

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count,total  #没有这一行会吧count和total变成局部变量local variable 'count' referenced before assignment
        count += 1
        total += new_value
        return total/count

    return averager

avg=make_average()
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)
print(avg(10))
print(avg(11))
print(avg(12))
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)


import time
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print("test")
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
    print(factorial.__name__)  #Python 解释器在背后会把 clocked 赋值给 factorial.现在 factorial 保存的是 clocked 函数的引用。
    print(factorial.__code__.co_varnames, factorial.__code__.co_freevars)


import time
import functools
def clock(func):
    @functools.wraps(func)  #functools.wraps 装饰器把相关的属性从 func 复制到 clocked 中。
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
        arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked

@clock
def factorial(n,test1="test1",test2="test2"):
    return 1 if n < 2 else n*factorial(n-1)

print(factorial.__name__)
print(factorial.__code__.co_varnames, factorial.__code__.co_freevars)

# 书上说标准库中最值得注意的两个装饰器是lru_cache和singledispatch  第一个是用在递归的。第二个是用在web上的。反正我现在并不需要
# 装饰器工厂 参数化装饰器 层级装饰器  工业级装饰器 类装饰器 singledispatch泛函数 __call__来实现装饰器   函数装饰函数  函数装饰类  类装饰函数 类装饰类
# 到此为止。所知道的收获就是装饰器工厂返回的是一个装饰器。这个工厂函数是按照函数调用的  @register 工厂函数必须作为函数调用，并且传入所需的参数。
# 装饰器的赋值其实是保留着引用，把被装饰的函数替换成新函数，二者接受相同
# 的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。  看完书在来总结吧。类装饰器就是__call__来实现的。很好


'''


