# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/1 2:59 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_7_9.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#你有一个除 __init__() 方法外只定义了一个方法的类。为了简化代码，你想将它转换成一个函数。 --闭包

'''
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.formap(kwargs))
    return opener
'''

#简单来讲，一个闭包就是一个函数， 只不过在函数内部带上了一个额外的变量环境。闭包关键特点就是它会记住自己被定义时的环境。 因此，在我们的解决方案中，opener() 函数记住了 template 参数的值，并在接下来的调用中使用它。