# 字符串对齐

#format比百分号和ljust(),rjust(),center()更有效。因为可以格式任意对象

text='hello world'
print(text.ljust(20))
print(text.rjust(20))
print(text.center(20))
print(text.rjust(20,'='))
print(text.center(20,'*'))
print(format(text,'>20'))
print(format(text,'<20'))
print(format(text,'^20'))
print(format(text,'=>20'))
print(format(text,'*^20'))

print('{:>10s} {:10>10s}'.format('hello','world'))  #{}之间要有空格
x=1.22345
print(format(x,'>10'))
print(format(x,'^10.2f'))


'''
hello world         
         hello world
    hello world     
=========hello world
****hello world*****
         hello world
hello world         
    hello world     
=========hello world
****hello world*****

'''