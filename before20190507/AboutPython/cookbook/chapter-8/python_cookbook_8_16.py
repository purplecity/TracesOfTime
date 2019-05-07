# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/14 3:05 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_16.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 在类中定义多个构造器   #classmethod

import time

class letsee:
    def __init__(self,a,b,c):
        print('hehe')

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

    @classmethod
    def today(cls):
        t=time.localtime()
        return cls(t.tm_year,t.tm_mon,t.tm_mday)



a=Date(2012,12,21)
b=Date.today()  #cls， 表示调用当前的类名。

print(b)  #<__main__.Date object at 0x102bab0b8>


#还是怀念之前讲的super mro   子类父类的dict dir属性探测 描述符的隐式转换这三个东东