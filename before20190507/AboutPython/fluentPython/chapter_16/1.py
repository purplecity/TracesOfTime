# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/2/28 4:55 PM                               
#  Author           purplecity                                       
#  Name             1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

from inspect import getgeneratorstate
def simple_coro2(a):
    print("->started:a=",a)
    b=yield  a
    print("is ka?")
    print("-> Received:b=",b)
    c=yield  a+b
    print("-> received:c=",c)

test=simple_coro2(14)
print(getgeneratorstate(test))
next(test)
print(getgeneratorstate(test))
test.send(28)


