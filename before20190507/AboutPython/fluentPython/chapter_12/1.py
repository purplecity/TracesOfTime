# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/2/28 2:31 PM                               
#  Author           purplecity                                       
#  Name             1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 子类话内置类型的缺点。 多重继承和方法解析顺序

# 1 其实就是内置类型会忽略用户覆盖的方法。就去继承collection中的类比如UserDict,MutableMaping等

# 还是__mro__