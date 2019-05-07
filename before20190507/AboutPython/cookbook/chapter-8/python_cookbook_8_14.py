# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/13 9:08 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_14.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

'''
你想实现一个自定义的类来模拟内置的容器类功能，比如列表和字典。但是你不确定到底要实现哪些方法。
collections
'''

import collections
import bisect

#其实就是集成collections中的基类