# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/8 3:20 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_11.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#你写了很多仅仅用作数据结构的类，不想写太多烦人的 __init__() 函数

# 解决方案 可以在一个基类中写一个公用的 __init__() 函数

# 类的dict和实例的dict，以及self不self。继承不继承的观察

import math
class Structure1:
    _fields=[]

    def __init__(self,*args):

        self.testvar=0
        if len(args) != len(self._fields):
            raise  TypeError('expected {} arguments'.format(len(self._fields)))
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
    def test2(self):
        self.testyyyyy=3

class Stock(Structure1):
    _fields = ['name','shares','price']

class Point(Structure1):
    _fields = ['x','y']

class Circle(Structure1):
    _fields = ['radius']
    def area(self):
        return math.pi * self.radius **2

class test(Structure1):
    m=5
    def txt(self):
        print('hehe')

print(Structure1.__dict__)
print(Stock.__dict__)
print(Point.__dict__)
print(Circle.__dict__)
print(test.__dict__) #没有field和testvar都继承不过来

'''
{'__module__': '__main__', '_fields': [], '__init__': <function Structure1.__init__ at 0x107e11d08>, 'test2': <function Structure1.test2 at 0x107e11d90>, '__dict__': <attribute '__dict__' of 'Structure1' objects>, '__weakref__': <attribute '__weakref__' of 'Structure1' objects>, '__doc__': None}
{'__module__': '__main__', '_fields': ['name', 'shares', 'price'], '__doc__': None}
{'__module__': '__main__', '_fields': ['x', 'y'], '__doc__': None}
{'__module__': '__main__', '_fields': ['radius'], 'area': <function Circle.area at 0x107e11e18>, '__doc__': None}
{'__module__': '__main__', 'txt': <function test.txt at 0x107e11ea0>, '__doc__': None}

#说明只要在类中除了init外出现过得变量和函数都会出现在方法中。 类中函数之外的地方不能有self.xxx的定义。
#子类的dict中没有test2方法 只有dir的才有。test类的dict也没有field属性。说明子类的dict方法中不会有父类的变量和函数

'''

a=Structure1()
b=Stock('ACME', 50, 91.1)
#b.test2()
c=Point(2,3)
d=Circle(4.5)
e=test()
#e.test2()
print(a.__dict__) #{'testvar': 0} 没有filed 实例来说带self的才是自己的dict中的属性。
print(b.__dict__)
print(c.__dict__)
print(d.__dict__)
print(e.__dict__)

print(dir(a))
print(dir(b))
print(dir(c))
print(dir(d))
print(dir(e))

#print(e._fields)  #[]
#print(e.m)  #5

'''
{'testvar': 0}
{'testvar': 0, 'name': 'ACME', 'shares': 50, 'price': 91.1}
{'testvar': 0, 'x': 2, 'y': 3}
{'testvar': 0, 'radius': 4.5}
{'testvar': 0}

有m有test2
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_fields', 'test2', 'testvar']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_fields', 'name', 'price', 'shares', 'test2', 'testvar']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_fields', 'test2', 'testvar', 'x', 'y']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_fields', 'area', 'radius', 'test2', 'testvar']
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_fields', 'm', 'test2', 'testvar', 'txt']

如果调用了b.test2()会多一个testyyyy的属性
因为有了setattr所有多了写属性。
{'testvar': 0}
{'testvar': 0, 'name': 'ACME', 'shares': 50, 'price': 91.1, 'testyyyyy': 3}
{'testvar': 0, 'x': 2, 'y': 3}
{'testvar': 0, 'radius': 4.5}
{'testvar': 0,'testyyyyy': 3}


说明子类的dict中只会有self.xxx的属性。函数方法没有在dict中。但是可以用.调用。好奇怪。

print(e._fields)  #[]
print(e.m)  #5 
'''

# 继承还是可以继承的，不管是类变量还是函数。b.x。默认是去dir(b)中找方法的，因为可能继承
# 但是类的dict  只要在类中除了init外出现过得变量和函数都会出现在方法中  子类的dict方法中不会有父类的变量和函数
# 实例dict     只会出现变量而且是self的变量。函数和不是self的变量都不会出现在dict中。但是都可以实例.变量或者函数调用。因为dir(实例)有

'''
#include <iostream>
using namespace std;

class Parent
{
public:
	Parent(int x, int y)
	{
		a = x;
		b = y;
	}

protected:

private:
	int a;
	int b;
};

class Child : public Parent
{
public:
	//给基类构造函数传参，必须通过参数列表
	Child(int x, int y, int z) : Parent(y, z)
	{
		c = x;
	}

private:
	int c;
};

class Test : Child
{
public:
	Test(int m, int x, int y, int z) : Child(x, y, z)
	{
		d = m;
	}

private:
	int d;
};

int main()
{
	//创建子类对象, 给对象中的成员变量初始化
	//除了本身新增加的数据，还有继承过来的数据
	//除了给自身初始化，还得给基类的构造函数传参
	Child obj(1, 2, 3);

	return 0;

'''

#因为子类继承父类的时候c++是要给父类构造函数传参的先父类构造函数然后调用子类构造函数。
# 然后因为这里调用的父类的构造函数。所以。操作是。给父类传0参。然后给子类传相应的参数。而且bcde都是共同使用父类的构造函数。子类实例化时候并没有创建父类的实例。只是继承过来了方法属性。
# 啊这两章真的是意犹未尽