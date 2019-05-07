# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/15 10:57 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_20.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#operator.methodcaller

import math
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __repr__(self):
        return 'Point({!r:},{!r:})'.format(self.x,self.y)

    def distance(self,x,y):
        return math.hypot(self.x-x,self.y-y)


p=Point(2,3)
d=getattr(p,'distance')(0,0)
print(d)

import operator
print(operator.methodcaller('distance',0,0)(p))

points = [
    Point(1, 2),
    Point(3, 0),
    Point(10, -3),
    Point(-5, -7),
    Point(-1, 8),
    Point(3, 2)
]

points.sort(key=operator.methodcaller('distance',0,0))
print(points)

m=Point(3,45)
d=operator.methodcaller('distance',0,0)
print(d(p))

'''

调用一个方法实际上是两部独立操作，第一步是查找属性，第二步是函数调用。 因此，为了调用某个方法，你可以首先通过 getattr() 来查找到这个属性，然后再去以函数方式调用它即可。

operator.methodcaller() 创建一个可调用对象，并同时提供所有必要参数， 然后调用的时候只需要将实例对象传递给它即可，
'''
