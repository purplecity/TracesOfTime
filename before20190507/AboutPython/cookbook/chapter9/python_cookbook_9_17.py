# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/21 10:27 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_17.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 你的程序包含一个很大的类继承体系，你希望强制执行某些编程规约（或者代码诊断）来帮助程序员保持清醒。

#  这章读一读比敲更好

'''
class NoMixedCaseMeta(type):
    def __new__(cls, clsname,bases,clsdict):  #默认会出现*args 和 **kwargs这样就忽略了clsname bases clsdict这样的形成其他类的时候重要信息了。
        print(type(clsdict))
        for name in clsdict:
            if name.lower() != name:
                raise TypeError("Bad attribute name:" + name)
        return super().__new__(cls,clsname,bases,clsdict)


class Root(metaclass=NoMixedCaseMeta):  pass

class A(Root):
    def foo_bar(self): pass

class B(Root):
    def fooBar(self): pass
'''



from inspect import signature
import logging

class MatchSignaturesMeta(type):
    def __init__(self,clsname,bases,clsdict):
        super().__init__(clsname,bases,clsdict)
        print(clsdict)
        print(self)
        print(self.__mro__)
        print(self.mro())
        sup=super(self,self)
        print("*"*3,dir(sup))
        print(sup)
        for name,value in clsdict.items():
            if name.startswith("_") or not callable(value): continue
            print(name,value)
            prev_dfn=getattr(sup,name,None)
            print(prev_dfn)

            if prev_dfn:
                prev_sig=signature(prev_dfn)
                val_sig=signature(value)
                if prev_sig != val_sig:
                    logging.warning('Signature mismatch in %s. %s != %s',
                                    value.__qualname__, prev_sig, val_sig)

class Root(metaclass=MatchSignaturesMeta): pass


class A(Root):
    def foo(self,x,y): pass
    def spam(self,x,*,z): pass

'''
{'__module__': '__main__', '__qualname__': 'Root'}
<class '__main__.Root'>
(<class '__main__.Root'>, <class 'object'>)
[<class '__main__.Root'>, <class 'object'>]
*** ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
<super: <class 'Root'>, <Root object>>
{'__module__': '__main__', '__qualname__': 'A', 'foo': <function A.foo at 0x10a59d158>, 'spam': <function A.spam at 0x10a59d1e0>}
<class '__main__.A'>
(<class '__main__.A'>, <class '__main__.Root'>, <class 'object'>)
[<class '__main__.A'>, <class '__main__.Root'>, <class 'object'>]
*** ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
<super: <class 'A'>, <A object>>
foo <function A.foo at 0x10a59d158>
None
spam <function A.spam at 0x10a59d1e0>
None  

这两个None是因为Root class没有foo 和spam方法
'''



class B(A):
    def foo(self,a,b): pass
    def spam(self,x,*,y): pass



'''

{'__module__': '__main__', '__qualname__': 'Root'}
WARNING:root:Signature mismatch in B.foo. (self, x, y) != (self, a, b)
<class '__main__.Root'>
(<class '__main__.Root'>, <class 'object'>)
WARNING:root:Signature mismatch in B.spam. (self, x, *, z) != (self, x, *, y)
[<class '__main__.Root'>, <class 'object'>]
*** ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
<super: <class 'Root'>, <Root object>>
{'__module__': '__main__', '__qualname__': 'A', 'foo': <function A.foo at 0x10fa7c0d0>, 'spam': <function A.spam at 0x10fa7c158>}
<class '__main__.A'>
(<class '__main__.A'>, <class '__main__.Root'>, <class 'object'>)
[<class '__main__.A'>, <class '__main__.Root'>, <class 'object'>]
*** ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
<super: <class 'A'>, <A object>>
foo <function A.foo at 0x10fa7c0d0>
None
spam <function A.spam at 0x10fa7c158>
None
{'__module__': '__main__', '__qualname__': 'B', 'foo': <function B.foo at 0x10fa7c1e0>, 'spam': <function B.spam at 0x10fa7c268>}
<class '__main__.B'>
(<class '__main__.B'>, <class '__main__.A'>, <class '__main__.Root'>, <class 'object'>)
[<class '__main__.B'>, <class '__main__.A'>, <class '__main__.Root'>, <class 'object'>]
*** ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
<super: <class 'B'>, <B object>>
foo <function B.foo at 0x10fa7c1e0>
<function A.foo at 0x10fa7c0d0>
spam <function B.spam at 0x10fa7c268>
<function A.spam at 0x10fa7c158>
'''

#意思是相同函数 签名相同？

#懂了super 的返回值的super对应的就是第二个参数此刻所在的mro列表中当前所在位置的前一个  妈的这得要3个类才行
# 妈的 这种单纯的继承super还好说。9-13那种super跟元类结合的是真蛋疼搞不清楚
