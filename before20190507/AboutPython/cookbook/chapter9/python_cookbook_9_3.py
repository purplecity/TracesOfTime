# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/16 7:02 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_3.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#解除一个装饰器

from functools import wraps

# 算了反正现在不能用countdown.__wrapper__()去访问被装饰的的函数。 前面的countdown是已经被转化过得countdown
# 这一章就是说明不可取的  并不是所有的装饰器都使用了 @wraps
# 特别的，内置的装饰器 @staticmethod 和 @classmethod 就没有遵循这个约定 (它们把原始函数存储在属性 __func__ 中)