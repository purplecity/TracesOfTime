# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/7 3:38 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_7.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 你想在子类中调用父类的某个已经被覆盖方法   super
'''
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()

# super() 函数的一个常见用法是在 __init__() 方法中确保父类被正确的初始化了：

class A:
    def __init__(self):
        self.x=0

class B(A):
    def __init__(self):
        super().__init__()
        self.y=1

    super() 的另外一个常见用法出现在覆盖Python特殊方法的代码中
'''

class Proxy:
    def __init__(self,obj):
        self._obj=obj

    def __getattr__(self, item):
        return getattr(self._obj,item)

    def __setattr__(self, key, value):
        if key.statswith('_'):
            super().__setattr__(key,value)

        else:
            setattr(self._obj,key,value)

# super对于多继承。卧槽最后亮了。super继承的本质 ORM顺序666.关键是MRO列表上继续搜索下一个类。并不一定是父类是MRO列表的下一个类
# 6666

