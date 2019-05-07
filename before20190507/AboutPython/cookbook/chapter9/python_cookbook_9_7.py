# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/17 1:57 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_7.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 利用装饰器强制函数上的类型检查

from inspect import signature
from functools import wraps

def typeassert(*ty_args,**ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func
        sig=signature(func)  #func形参
        print(sig,type(sig),dir(sig))
        print(sig.parameters)
        print(sig.parameters['z'],sig.parameters['z'].default,sig.parameters['z'].kind)
        bound_types=sig.bind_partial(*ty_args,**ty_kwargs).arguments  #获取装饰器传来的参数与sig(func的形参# )绑定
        #bind() 跟 bind_partial() 类似，但是它不允许忽略任何参数。
        print(bound_types,type(bound_types),bound_types.__dict__)


        @wraps(func)
        def wrapper(*args,**kwargs):
            bound_values=sig.bind(*args,**kwargs)  #实参
            print(bound_values,type(bound_values))
            for name ,value in bound_values.arguments.items():
                if name in bound_types:  #key可以直接in来操作？
                    if not isinstance(value,bound_types[name]):


                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper


    return decorate

@typeassert(int,z=int)
def spam(x,y,z=42):
    print(x,y,z)

#如果没有实例化。不会调用包装器中的东东，装饰器只会在函数定义时被调用一次,wrapper就是接受实参的

spam(3,3,z=8)
spam(3,'hehe',z=9)
'''
(x, y, z=42) <class 'inspect.Signature'> ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_bind', '_bound_arguments_cls', '_hash_basis', '_parameter_cls', '_parameters', '_return_annotation', 'bind', 'bind_partial', 'empty', 'from_builtin', 'from_callable', 'from_function', 'parameters', 'replace', 'return_annotation']
OrderedDict([('x', <Parameter "x">), ('y', <Parameter "y">), ('z', <Parameter "z=42">)])
OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)]) <class 'collections.OrderedDict'> {}
<BoundArguments (x=3, y=3, z=8)> <class 'inspect.BoundArguments'>
3 3 8

'''