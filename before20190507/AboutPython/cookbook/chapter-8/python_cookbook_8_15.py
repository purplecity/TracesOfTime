# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/14 2:33 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_15.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#属性的代理访问
#将某个实例的属性访问代理到内部另一个实例中去。
#将某个操作转移给另外一个对象来实现

class A:
    def spam(self,x): print(x)
    def foo(self): pass

class B1:
    def __init__(self):
        self._a=A()

    def spam(self,x): return self._a.spam(x)

    def foo(self): return self._a.foo()

    def bar(self): pass


class B2:
    def __init__(self): self._a=A()

    def bar(self): pass

    def __getattr__(self,name): return getattr(self._a,name)

b=B2()
b.bar()
b.spam(42)  #42  Calls B.__getattr__('spam') and delegates to A.spam  42作为参数传递

class Proxy:
    def __init__(self,obj): self._obj=obj

    def __getattr__(self, name):
        print('getattr:',name)
        return getattr(self._obj,name)

    def __setattr__(self, key, value):  #还记得用__setattr__有风险要集成object的详见python学习手册
        if key.startswith('_'):
            super().__setattr__(key,value)
        else:
            print('setattr:',key,value)
            setattr(self._obj,key,value)

    def __delattr__(self, item):
        if item.startswith('_'):
            super().__delattr__(item)
        else:
            print('delattr:',item)
            delattr(self._obj,item)


#如果类自定义了__setattr__方法，当通过实例获取属性尝试赋值（ 不存在的属性值）时，就会调用__setattr__。
#常规的对实例属性赋值，被赋值的属性和值会存入实例属性字典__dict__中。


class Spam:
    def __init__(self,x): self.x=x

    def bar(self,y):print('spam.bar:',self.x,y)

s=Spam(2)
p=Proxy(s)  #都是实例。拿实例初始化
print(p.x)
p.bar(3)
p.x=37  #对于p来说x是不存在的所以也会调用__setattr__
p.z=40

print(s.__dict__)

'''

42
getattr: x
2
getattr: bar
spam.bar: 2 3
setattr: x 37
setattr: z 40
{'x': 37, 'z': 40}'''



