# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/17 2:45 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_8.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#将装饰器定义为类的一部分
# 你想在类中定义装饰器，并将其作用在其他函数或者方法上


from functools import wraps

class A:
    def decorator1(self,func):  #实例方法
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('Decorator 1')
            return func(*args,**kwargs)
        return wrapper

    @classmethod
    def decorator2(cls,func): #类方法
        def wrapper(*args,**kwargs):
            print('Decorator 2')
            return func(*args,**kwargs)
        return wrapper


a=A()

@a.decorator1
def spam(): pass

@A.decorator2
def grok(): pass

x=grok()
print(type(x))
#我印象中遇到的都是classmethod如果有之前有init或者__new__调用会返回实例。这里是啥也不反回。只是一个类方法。也可以吧。。。
#None是Python的特殊类型，NoneType对象，它只有一个值None.

class B(A):
    @A.decorator2  #A的类方法被做成装饰器还是必须显式父类调用
    def bar(self): pass

m=B()
m.bar()


# 因此，任何时候只要你碰到需要在装饰器中记录或绑定信息 就可以这样