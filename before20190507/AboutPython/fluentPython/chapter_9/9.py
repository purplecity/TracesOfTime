# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/30 5:50 PM                               
#  Author           purplecity                                       
#  Name             9.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 要想一个对象可hash必须实现 __hash__  __eq__
# python对象对__有严格的要求。但是对_没有要求，全靠自觉---自己定的规则比双下划线易于理解。
'''
一个特殊的属
性（不是方法），它会影响对象的内部存储，对内存用量可能也有重大
影响，不过对对象的公开接口没什么影响。这个属性是 __slots__。

默认情况下，Python 在各个实例中名为 __dict__ 的字典里存储实例属
性。如 3.9.3 节所述，为了使用底层的散列表提升访问速度，字典会消
耗大量内存。如果要处理数百万个属性不多的实例，通过 __slots__
类属性，能节省大量内存，方法是让解释器在元组中存储实例属性，而
不用字典。

继承自超类的 __slots__ 属性没有效果。Python 只会使用
各个类中定义的 __slots__ 属性。

在类中定义 __slots__ 属性的目的是告诉解释器：“这个类中的所有实
例属性都在这儿了！

定义 __slots__ 的方式是，创建一个类属性，使用 __slots__ 这个名
字，并把它的值设为一个字符串构成的可迭代对象，其中各个元素表示
各个实例属性



在类中定义 __slots__ 属性之后，实例不能再有
__slots__ 中所列名称之外的其他属性。这只是一个副作用，不是
__slots__ 存在的真正原因。不要使用 __slots__ 属性禁止类的
用户新增实例属性。__slots__ 是用于优化的，不是为了约束程序
员。


'''



#p413
# 类，子类，实例---覆盖属性问题--非方法。这里讲的是属性。没毛病
#
#
# self.xxx xxx
