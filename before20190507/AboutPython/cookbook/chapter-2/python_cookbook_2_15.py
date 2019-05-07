# 在字符串中插入变量

s='{name} has {n} messages'
print(s.format(name='hehe',n=37))

# 暂时抛弃vars()这个变量域参数。有很多的获取变量的方法。

# print(s.format(name='hhe'))  会报错.因为不能丢弃变量

print('{:,}'.format(9987733498273.0432)) #9,987,733,498,273.043
print('{:,}'.format(987733498273.0432)) #987,733,498,273.0432
print('{:,}'.format(87733498273.04325))   #87,733,498,273.04324
print('{:,}'.format(987733498273.04325)) #987,733,498,273.0432
print('{:,}'.format(733498273.04325666)) #733,498,273.0432566

class Missing(dict):
    def __missing__(self, key):
        return 'missing'

d=Missing()
print(d['hehe'])  #missing


'''
format大全
Python之format详解

1.通过位置

'a1 = {} a2= {}  a3= {}'.format('first','second','third')  #{}不带参数
'a1 = first a2= second  a3= third'
'a1 = {1} a2= {0}  a3= {2}'.format('first','second','third') #{}带位置参数的
'a1 = second a2= first  a3= third'
注意如果{}要带参数，可以将format看成一个函数输入的值是函数的参数，这些输入的值可以看成一个元组，{0} == tuple[0] 同样他们也不能越界
2.通过关键字参数

'your name is {name} , age is {age}'.format(name='jack',age=87)
'your name is jack , age is 87'
'your name is {name} , age is {age}'.format(age=87,name='jack') #同样和位置无关
'your name is jack , age is 87'
3.通过对象属性

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

p = Person('Tom',18)
'name = {p.name} age = {p.age}'.format(p=p)
'name = Tom age = 18'
4.通过下标

s1 = [1,'23','tom']
s2 = ['s2.1','s2.2','s2.3']
'{0[1]}  {0[2]} {1[2]} {1[0]}'.format(s1,s2)
'23  tom s2.3 s2.1'
5.格式化输出(重点)

 格式限定符
 语法是{}中带:号）
 {:对齐方式  填充}
 填充与对齐
 填充常跟对齐一起使用
 ^、<、>分别是居中、左对齐、右对齐，后面带宽度
 :号后面带填充的字符，只能是一个字符，不指定的话默认是用空格填充
5.1对齐与填充

'输出左对齐定长为10位  [{:<10}]'.format('12') #默认填充空格的
'输出左对齐定长为10位  [12        ]'
'输出右对齐定长为10位  [{:>10}]'.format('12') #默认填充空格的
'输出右对齐定长为10位  [        12]'
'输出右对齐定长为10位  [{:0>10}]'.format('12') #修改填充，填充只能是一个ASCII字符
'输出右对齐定长为10位  [0000000012]'
'输出居中对齐定长为10位，填充x  [{:x^10}]'.format('12') #修改填充，填充只能是一个ASCII字符
'输出居中对齐定长为10位，填充x  [xxxx12xxxx]'
5.2浮点小数输出

'{:.2f}'.format(1233442.23453) #通常都是配合 f 使用,其中.2表示长度为2的精度，f表示float类型
'1233442.23'
'{:,}'.format(9987733498273.0432) #使用逗号金额分割符
'9,987,733,498,273.043'
5.3进制及其他显示

b : 二进制
d ：十进制
o ：八进制
x ：十六进制
!s ：将对象格式化转换成字符串
!a ：将对象格式化转换成ASCII
!r ：将对象格式化转换成repr
'10 二进制 ：{:b}'.format(10)
'10 二进制 ：1010'
'10 十进制 ：{:d}'.format(10)
'10 十进制 ：10'
'10 八进制 ：{:o}'.format(10)
'10 八进制 ：12'
'10 十六进制 ：{:x}'.format(10)
'10 十六进制 ：a'
'{!s}'.format(10) #格式化转换
'10'
'{!a}'.format('1000') #格式化转换
"'1000'"
'{!r}'.format('1000') #格式化转换
"'1000'"

'''
