# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/3/5 4:06 PM                               
#  Author           purplecity                                       
#  Name             1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

'''

在 Python 中，数据的属性和处理数据的方法统称属性（attribute）。其
实，方法只是可调用的属性。除了这二者之外，我们还可以创建特性
（property），在不改变类接口的前提下，使用存取方法（即读值方法
和设值方法）修改数据属性。

'''

class Quantity: ➊
    def __init__(self, storage_name):
        self.storage_name = storage_name ➋
    def __set__(self, instance, value): ➌
        if value > 0:
            instance.__dict__[self.storage_name] = value ➍
        else:
            raise ValueError('value must be > 0')

class LineItem:
    weight = Quantity('weight') ➎
    price = Quantity('price') ➏

    def __init__(self, description, weight, price): ➐
        self.description = description
        self.weight = weight
        self.price = price
    def subtotal(self):
        return self.weight * self.price



# 算了提前宣告本书完结。 接下来就是总结。  asyncio 迭代 装饰器  描述符 元类等等觉得自己不懂但是有必要的