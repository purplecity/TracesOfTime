# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/7 10:59 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_4.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 创建大量对象时节省内存方法

class Date:
    __slots__ = ['year','month','day']
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

#没啥好讲的，想把全部复制过来。__slots__ 更多的是用来作为一个内存优化工具。
#当你定义 __slots__ 后，Python就会为实例使用一种更加紧凑的内部表示。 实例通过一个很小的固定大小的数组来构建，而不是为每个实例定义一个字典，这跟元组或列表很类似。 在 __slots__ 中列出的属性名在内部被映射到这个数组的指定小标上。 使用slots一个不好的地方就是我们不能再给实例添加新的属性了，只能使用在 __slots__ 中定义的那些属性名。
# 尽管slots看上去是一个很有用的特性，很多时候你还是得减少对它的使用冲动。 Python的很多特性都依赖于普通的基于字典的实现。 另外，定义了slots后的类不再支持一些普通类特性了，比如多继承。


