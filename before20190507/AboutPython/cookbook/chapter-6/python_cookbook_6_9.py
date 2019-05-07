# 将一个十六进制字符串解码成一个字节字符串或者将一个字节字符串编码成一个十六进制字符串。

s=b'hello'
print(len(s))

import binascii
h=binascii.b2a_hex(s)  #编码
print(h)  #b'68656c6c6f'
print(binascii.a2b_hex(h))  #b'hello'
print(binascii.a2b_hex(h).decode('ascii')) #hello  str与bytes之间的转换

# b'68656c6c6f'  16进制68转换为2进制为1101000 转化为10进制为104 对应字符'h'

# 参数
# *args接收的可变参数，f(1,2,3...)会把参数组成一个tuple。 *可以解压list或者tuple
# **kwgs 接收的是=  F(a=1,b=2,c=3) 这些关键字参数在函数内部自动组装为一个dict **可以解压dict

def person(name,age,**kw):
    print('name:',name,'age:',age,'other:',kw)

person('Adam',45,gender='M',job='engineer')
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('jack',40,city=extra['city'],job=extra['job'])
person('jack',40,**extra)

'''
name: Adam age: 45 other: {'gender': 'M', 'job': 'engineer'}
name: jack age: 40 other: {'city': 'Beijing', 'job': 'Engineer'}
name: jack age: 40 other: {'city': 'Beijing', 'job': 'Engineer'}
'''


