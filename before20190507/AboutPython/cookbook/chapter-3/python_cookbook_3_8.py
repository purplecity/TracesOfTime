# fractions

from fractions import Fraction

a=Fraction(5,4) # 分子，分母
b=Fraction(7,16)
c=a*b
print(a+b,a*b)
print(c.numerator)  #分子
print(c.denominator) #分母
print(float(c))
x=3.75
print(Fraction(*x.as_integer_ratio()))

'''
27/16 35/64
35
64
0.546875
15/4

'''