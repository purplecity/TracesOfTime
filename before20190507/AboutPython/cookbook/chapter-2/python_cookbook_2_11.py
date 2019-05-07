# 删除不需要的字符

# strip() 方法能用于删除开始或结尾的字符。 lstrip() 和 rstrip() 分别从左和从右执行删除操作,默认情况下，这些方法会去除空白字符，但是你也可以指定其他字符
# 但是字符串中间的字符却没有去除
s=' hello world \n'
print(s.strip())
print( s.lstrip())
print(s.rstrip())

t='------hello====='
print(t.lstrip('-'))
print(t.strip('-='))
'''

hello world
hello world 

 hello world
hello=====
hello
'''
import re
print(s.replace(' ',''))  #helloworld
print(re.sub('\s+',' ',s)) #把连续几段空格变为一个空格  hello world
