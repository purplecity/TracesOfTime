# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/2/28 2:16 PM                               
#  Author           purplecity                                       
#  Name             1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import abc

class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self,iterable):
        '''从可迭代对象中添加元素'''

    @abc.abstractmethod
    def pick(self):
        '''随机删除元素，然后将其返回。如果实例为空，这个方法应该抛出`LookupError`'''

    def loaded(self):
        '''如果至少有一个元素，返回`True`，否则返回`False`'''
        return bool(self.inspect())

    def inspect(self):
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break

        self.load(items)
        return tuple(sorted(items))


from random import randrange

@Tombola.register
class TomboList(list):
