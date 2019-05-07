# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/14 5:04 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_18.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Mixins 混入类 就是多继承-=-=  不是说好的装饰器更好吗-。=
# 你有很多有用的方法，想使用它们来扩展其他类的功能。但是这些类并没有任何继承的关系。因此你不能简单的将这些方法放入一个基类，然后被其他类继承

class LoggedMappingMixin:
    __slots__ = ()
    def __getitem__(self, item):
        print('Getting' + str(item))
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        print('setting {} = {!r}'.format(key,value))
        return super().__setitem__(key,value)
    def  __delitem__(self,key):
        print('deleting' + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    __slots__ = ()
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + 'already set')
        return super().__setitem__(key,value)

class StringKeysMappingMixin:
    __slots__ = ()
    def __setitem__(self, key, value):
        if not isinstance(key,str):
            raise TypeError('key must be strings')
        return super().__setitem__(key,value)


class LoggedDict(LoggedMappingMixin,dict):pass

d=LoggedDict()  #从左到右顺序继承。所以会调用LoggedMappingMixin的方法
d['x']=23
print(d['x'])
del d['x']

'''

setting x = 23
Gettingx
23
deletingx
'''

from collections import defaultdict

class SetOnceDefaultDict(SetOnceMappingMixin,defaultdict): pass

d=SetOnceDefaultDict(list)   #d的每一个值都是一个list类型 详情如下以及可以搜索 defaultdict(list)
d['x'].append(2)
d['x'].append(3)
d['y'].append(4)
print(d['x'])  #[2, 3]
print(d['y'])
print(d.__dict__)  #{}

'''

这里的defaultdict(function_factory)构建的是一个类似dictionary的对象，其中keys的值，自行确定赋值，但是values的类型，是function_factory的类实例，而且具有默认值。比如default(int)则创建一个类似dictionary对象，里面任何的values都是int的实例，而且就算是一个不存在的key, d[key] 也有一个默认值，这个默认值是int()的默认值0.
'''
'''
[2, 3]
[4]
{}
'''

#到现在的目的： mixin就是增强已存在的类的功能和一些可选特征。就是多继承的应用，只是可以用类装饰器实现混入类
def LoggedMapping(cls):
    cls_getitem = cls.__getitem__
    cls_setitem = cls.__setitem__
    cls_delitem = cls.__delitem__

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return cls_getitem(self, key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return cls_setitem(self, key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return cls_delitem(self, key)

    cls.__getitem__ = __getitem__
    cls.__setitem__ = __setitem__
    cls.__delitem__ = __delitem__
    return cls


@LoggedMapping
class LoggedDict(dict):
    pass

m=LoggedDict()  #从左到右顺序继承。所以会调用LoggedMappingMixin的方法
m['x']=23
print(m['x'])
del m['x']

'''
Setting x = 23
Getting x
23
Deleting 一样的效果
'''