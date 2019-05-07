# 反向迭代

# reversed()方法当对象的大小可预先确定或者对象实现了 __reversed__() 的特殊方法时才能生效。 如果两者都不符合，那你必须先将对象转换为一个列表才行,会占内存

a=[1,2,3,5,6]
for x in reversed(a):
    print(x)

'''
f=open('somefile')
for line in reversed(list(f)):
    print(line)
'''

#自定义类上实现 __reversed__() 方法来实现反向迭代

class Countdown:
    def __init__(self,start):
        self._start=start

    def __iter__(self):
        n=self._start
        while n>0:
            yield  n
            n -= 1
    def __reversed__(self):
        n=1
        while n<= self._start:
            yield  n
            n += 1

for rr in reversed(Countdown(30)):
    print(rr)

for rr in Countdown(30):
    print(rr)
