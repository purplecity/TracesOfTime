# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/6 8:05 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_2.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


#format内置函数

# format(value[, format_spec])
# 　　1. 函数功能将一个数值进行格式化显示。
#
# 　　2. 如果参数format_spec未提供，则和调用str(value)效果相同，转换成字符串格式化。


'''

format(value[, format_spec])

Convert a value to a “formatted” representation, as controlled by format_spec. The interpretation of format_spec will depend on the type of the value argument, however there is a standard formatting syntax that is used by most built-in types: Format Specification Mini-Language.

The default format_spec is an empty string which usually gives the same effect as calling str(value).

A call to format(value, format_spec) is translated to type(value).__format__(value, format_spec) which bypasses the instance dictionary when searching for the value’s __format__() method. A TypeError exception is raised if the method search reaches object and the format_spec is non-empty, or if either the format_spec or the return value are not strings.


__format__()方法
　　__format__()传参方法：someobject.__format__(someobject,specification)

　　specification为指定格式，当应用程序中出现"{0:specification}".format(someobject)或format(someobject, specification)时，会默认以这种方式调用

　　当specification为" "时，一种合理的返回值是return str(self),这为各种对象的字符串表示形式提供了明确的一致性

　　注意，"{0!s}".format()和"{0!r}".format()并不会调用__format__()方法，他们会直接调用__str__()或者__repr__()

'''

_formats={
    'ymd':'{d.year}-{d.month}-{d.day}',
    'mdy':'{d.month}/{d.day}/{d.year}',
    'dmy':'{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

    def __format__(self, code):
        if code == '':
            code='ymd'
        fmt=_formats[code]   #居然可以这样直接用变量我日。
        return fmt.format(d=self)

d=Date(2012,12,21)
print(format(d))
print(format(d,'mdy'))
print('THe date is {:ymd}'.format(d))  #:后接的是格式，意思是format(d,'ymd）

'''
着重强调的是格式化代码的解析工作完全由类自己决定。因此，格式化代码可以是任何值。 例如，参考下面来自 datetime 模块中的代码：

'''

from datetime import date
x=date(2012,12,21)
print(format(x))
print(format(x,'%A,%B %d,%Y'))
print('the end is {:%d %b %Y}. Goodbye'.format(x))

'''
2012-12-21
12/21/2012
THe date is 2012-12-21
2012-12-21
Friday,December 21,2012
the end is 21 Dec 2012. Goodbye
'''