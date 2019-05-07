# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/15 5:27 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_23.py
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#循环引用暂时用不到pass
# 原因是Python的垃圾回收机制是基于简单的引用计数。 当一个对象的引用数变成0的时候才会立即删除掉
import weakref
# weakref.ref可以解决这个问题