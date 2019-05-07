# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/25 4:09 PM                               
#  Author           purplecity                                       
#  Name             3.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#Python 里大多数映射类型的构造
#方法都采用了类似的逻辑，因此你既可以用一个映射对象来新建一个映
#射对象，也可以用包含 (key, value) 元素的可迭代对象来初始化一个
#映射对象。

import collections

class strKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key,str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, item):
        return str(item) in self.data

    def __setitem__(self, key, value):
        self.data[str(key)] = value

print(strKeyDict.__dict__)

from dis import dis #这个居然是用来反汇编的
# 字典在内存上的开销巨大，由于字典使用了散列表而散列表又是稀疏的。
#  ，不要对字典同时进行迭代和修改。如果想扫描并修改一
# 个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加
# 的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字
# 典进行更新。  字典的操作还是得去看cookbook