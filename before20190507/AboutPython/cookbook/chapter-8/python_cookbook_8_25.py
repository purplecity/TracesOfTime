# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/15 5:52 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_25.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 创建缓存实例
#在创建一个类的对象时，如果之前使用同样参数创建过这个对象， 你想返回它的缓存引用。

class Spam:
    def __init__(self,name):
        self.name=name

import weakref
_spam_cache=weakref.WeakKeyDictionary
def get_spam(name):
    if name not in _spam_cache:
        s=Spam(name)
        _spam_cache[name]=s

    else:
        s=_spam_cache[name]
    return s

a=get_spam('foo')
b=get_spam('bar')
print( a is b)
c=get_spam('foo')
print(a is c)


#还是最后一种方法舒服

class CachedSpamManager2:
    def __init__(self):
        self._cache=weakref.WeakKeyDictionary()

    def get_spam(self,name):
        if name not in self._cache:
            temp=Spam3._new(name)
            self._cache[name]=temp
        else:
            temp=self._cache[name]

        return temp
    def clear(self):
        self._cache.clear()


class Spam3:
    def __init__(self,*args,**kwargs):
        raise RuntimeError("can't instance directly")

    @classmethod
    def _new(cls,name):
        self=cls.__new__(cls)
        self.name=name
        return self
