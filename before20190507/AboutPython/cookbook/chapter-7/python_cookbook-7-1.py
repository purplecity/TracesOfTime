# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/1 10:33 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook-7-1.py
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 7-1 *args 是元组 **kwargs可变关键字参数是dict没啥好讲的 7-2没啥好说的  7-3没啥好说的  7-4没啥好说的  7-5 参数=None可以代表任意类型
# 7-6  lambda创建一个函数对象，冒号前面就是函数参数，做表达式的操作，等价于函数，返回值就是函数的值

'''
import sys
f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk)
'''

#iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记(结尾)值作为输入参数。 当以这种方式使用的时候，它会创建一个迭代器，
#  这个迭代器会不断调用 callable 对象直到callable返回值和标记值相等为止。

'''
names = ['David Beazley', 'Brian Jones','Raymond Hettinger', 'Ned Batchelder']
sorted(names, key=lambda name: name.split()[-1].lower())  #key是一个函数的返回值。然后sorted会把每一个元素传进去给name根据返回值key做排序，所以name不是names

x=10
a=lambda y,x: x+y
x=20
b=lambda  y,x: x+y
#a(10) b(10) 都是30  改为lambda y,x=x: x+y那么20，30  通过使用函数默认值参数形式，lambda函数在定义时就能绑定到值
'''

#function.partial都可以用lambda实现。只不过前者更加清晰。然后接受提前参数