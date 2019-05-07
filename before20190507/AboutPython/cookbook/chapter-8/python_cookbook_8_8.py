# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/7 9:24 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_8.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 在子类中你想要扩展第定义在父类的property功能

class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    def del_name(self):
        raise AttributeError("Can't delete attribute")

    x=property(get_name,set_name,del_name)

class SubPerson(Person):

    def get_name(self):
        print('getting name')
        return super().x

    def set_name(self, value):
        print('Setting name to', value)
        super(SubPerson,SubPerson).x=value

    def del_name(self):
        print('delete name')
        super(SubPerson,SubPerson).x.del_name(self)  #这里应该是用绑定父类去调用父类的方法

s=SubPerson("guidio")  #这个真的只是为了初始化父类的觉得

'''

    def __init__(self, type1=None, type2=None): # known special case of super.__init__
        """
        super() -> same as super(__class__, <first argument>)
        super(type) -> unbound super object
        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)
        Typical use to call a cooperative superclass method:
        class C(B):
            def meth(self, arg):
                super().meth(arg)
        This works for class methods too:
        class C(B):
            @classmethod
            def cmeth(cls, arg):
                super().cmeth(arg)
        
        # (copied from class doc)
'''



'''
def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]
其中，cls 代表类，inst 代表实例，上面的代码做了两件事：

获取 inst 的 MRO 列表
查找 cls 在当前 MRO 列表中的 index, 并返回它的下一个类，即 mro[index + 1]
当你使用 super(cls, inst) 时，Python 会在 inst 的 MRO 列表上搜索 cls 的下一个类。

感觉inst也可以是class暂时结合下面这样理解吧。就是返回inst 的mro列表的cls的下一个类。

综合        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)
'''

