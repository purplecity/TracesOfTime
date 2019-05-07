# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/18 3:13 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_12.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 重写类定义的某部分来修改它的行为，但是你又不希望使用继承或元类的方式。
# 使用装饰器扩展类的功能


#如果你系想在一个类上面使用多个类装饰器，那么就需要注意下顺序问题。 例如，一个装饰器A会将其装饰的方法完整替换成另一种实现， 而另一个装饰器B只是简单的在其装饰的方法中添加点额外逻辑。 那么这时候装饰器A就需要放在装饰器B的前面。


def log_getattribute(cls):
    orig_getattribute=cls.__getattribute__

    def new_getattrbute(self,name):
        print('getting:',name)
        return orig_getattribute(self,name)

    cls.__getattribute__=new_getattrbute
    return cls

@log_getattribute
class A:
    def __init__(self,x):
        self.x=x
    def spam(self):
        pass


a=A(42)
print(a.x)
a.spam()
'''
getting: x
42
getting: spam'''

