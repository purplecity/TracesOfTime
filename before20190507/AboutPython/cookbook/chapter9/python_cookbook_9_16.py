# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/21 9:02 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_16.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# *args **kwargs的强制参数签名

# 对任何涉及到操作函数调用签名的问题，都应该使用inspect中的签名特性。重点Signature Parameter

from inspect import Signature,Parameter

parms=[ Parameter("x",Parameter.POSITIONAL_OR_KEYWORD),
        Parameter("y",Parameter.POSITIONAL_OR_KEYWORD,default=42),
        Parameter("z",Parameter.KEYWORD_ONLY,default=None)]

sig=Signature(parms)  #  Signature对Parameter进行签名
#一旦你有了一个签名对象，你就可以使用它的 bind() 方法很容易的将它绑定到 *args 和 **kwargs 上去。
# 就是把函数参数跟自己设定的参数进行绑定。也有部分绑定的函数.还可以直接signature函数
'''
def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                            )
            return func(*args, **kwargs)
        return wrapper


'''

def func(*args,**kwargs):
    bound_values=sig.bind(*args,**kwargs)
    for name,value in bound_values.arguments.items():
        print(name,value)

func(1,2,z=3)
'''
x 1
y 2
z 3
'''

'''
def make_sig(*names):
    parms=[ Parameter(name,Parameter.POSITIONAL_OR_KEYWORD) for  name  in  names ]
    return Signature(parms)

class Structure:
    __signature__=make_sig()
    def __init__(self,*args,**kwargs):
        bound_values=self.__signature__.bind(*args,**kwargs)
        for name,value in bound_values.arguments.items():
            setattr(self,name,value)

class Stock(Structure):
    __signature__ = make_sig('name','shares','price')

class Point(Structure):
    __signature__ = make_sig("x","y")

import inspect
a=inspect.signature(Stock)
print(type(a))  #<class 'inspect.Signature'>
print(dir(a))
print(a)  ##(name, shares, price)
print(Stock.__signature__)  #(name, shares, price)  意思就是打印签名就是打印要进行签名的参数吗
#print(inspect.signature(Stock))  #对类签名？类中的__signature__已经是签过名了啊

'''

# 元类来创建签名对象


def make_sig(*names):
    parms=[ Parameter(name,Parameter.POSITIONAL_OR_KEYWORD) for  name  in  names ]
    return Signature(parms)

class StructureMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        clsdict['__signature__']=make_sig(*clsdict.get('_fileds',[]))
        return super().__new__(cls,clsname,bases,clsdict)


class Structure(metaclass=StructureMeta):
    _fields=[]
    def __init__(self,*args,**kwargs):
        bound_values=self.__signature__.bind(*args,**kwargs)
        for name,value in bound_values.arguments.items():
            setattr(self,name,value)


class Stock(Structure):
    _fields=['name','shares','price']

class Point(Structure):
    _fileds=['x','y']


#利用元类来创建签名对象真的是要对之前的原来__prepare__那个方法熟悉才行。这里的clsdict就是搜集的Structure类的属性
# 这继承的 意犹未尽