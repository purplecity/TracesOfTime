# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/8/4 10:27 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_zaqizaba_learn.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#python 学习手册第30章第31章

# 与c++的关系
# inti方法就是构造函数。继承就是抽象类用了纯虚函数。子类重写虚函数就调子类方法。子类可以调用父类方法。子类对象初始化的时候要初始化父类构造函数和其他类的构造函数才行
# 组合办事nice  python学习手册p745

'''
class Processor:
    def __init__(self,reader,writer):
        self._reader=reader
        self._writer=writer
    def process(self):
        while 1:
            data=self._reader.readline()
            if not data: break
            data=self.converter(data)
            self._writer.write(data)

    def converter(self,data):
        assert False,'converter must be defined'

class Upercase(Processor):
    def converter(self,data):
        return data.upper()

class HTMLize:
    def write(self,line):
        print('<PRE>%s</PRE>' % line.rstrip())

#converter write readline upper()都是事先不知道  公有python方法或者自定义方法
'''
'''
if __name__ == '__main__':
    import sys
    obj=Upercase(open('/Users/purplecity/letsee.log'),sys.stdout)
    obj.process()
    Upercase(open('/Users/purplecity/letsee.log'),HTMLize()).process()  
    #传入一个空的HTMLise对象

'''
'''
# 装饰器初步

class wrapper:
    def __init__(self,object):
        self.wrapped=object
    def __getattr__(self,attrname):
        print('Trace:',attrname)
        return getattr(self.wrapped,attrname)

x=wrapper([1,2,3])
print(x.append(4))
print(x.wrapped) #self.wrapped
y=wrapper({"a":1,"b":2})
print(y.keys())
'''
# __getattr__这个私有东东能  获得属性名称 字符串
#  利用 变量名字符串  从包裹对象取出属性
# getattr(X,N)就像是X.N 只不过N是表达式而不是变量
# getattr内置函数就是获取对象的属性的

# 控制器内有不同的对象。控制器把不同属性传给不同对象， __getattr__拦截  对不存在属性的读取

'''
class C1:
    def meth1(self): self.x=88
    def meth2(self): print(self.x)

class C2:
    def meth1(self): self.x=99
    def meth2(self): print(self.x)

class c3(C1,C2): ...

I=c3()  #不知道取哪个x

# 对C1 self.__x <=> self._C1_x
'''

'''
class Super:
    def method(self): print('super')

class Tool:
    def __method(self): print('Tool')
    def other(self): self.__method()  #自己的__method

class Sub1(Tool,Super):
    def actions(self): self.method()  # Super的method

class Sub2(Tool):
    def __init__(self):self.method=99  #只是一个变量值


# __dict__ 一个类实例所具有的属性的集合
# dir内置函数，除了类实例所具有的属性  还收集了所有继承的属性  #id内置函数就是返回对象的内存地址
'''

'''
class ListInherited:
    def __str__(self):
        return '< Instance of %s ,address %s:\n%s>' % (self.__class__.__name__,id(self),self.__attrnames)

    def __attrnames(self):
        result=''
        for attr in dir(self):
            if attr[:2] == '__' and attr[-2:]:
                result += '\t name %s=<>\n' % attr
            else:
                 result += '\t name %s=%s\n' % (attr,getattr(self,attr))

        return result

#用__dict__列出实例属性就是这样
for attr in sorted(self.__dict__):
    result += '\t name %s=%s \n' % (attr,self.__dict__ [attr]')
    return result

'''

# 列出类树种每个对象的属性
'''
class ListTree:
    def __str__(self):
        self.__visited={}
        return '<Instance of {0},address {1}:\n{2}{3}>'.format(self.__class__.__name__,id(self),self.__attrnames(self,0),self.__listclass(self.__class__,4))

    def __listclass(self,aClass,indent):
        dots='.'*indent  #打印4个小数点
        if aClass in self.__visited:
            return '\n{0}<Class {1}:,address {2}:(see above) >\n'.format(dots,aClass.__name__,id(aClass))
        else:
            self.__visited[aClass]=True
            genabove=(self.__listclass(c,indent+4) for c in aClass.__bases__)
            return '\n{0}<Class {1},addreess {2}: \n{3}{4}{5}>\n'.format(dots,aClass.__name__,id(aClass),self.__attrnames(aClass,indent),''.join(genabove),dots)


    def __attrnames(self,obj,indent):
        spaces=' '* (indent + 4)
        result=''
        for attr in sorted(obj.__dict__):
            if attr.startswith('__') and attr.endswith('__'):
                result += spaces + '{0}=<>\n'.format(attr)
            else:
                result += spaces + '{0}={1}\n'.format(attr,getattr(obj,attr))
        return result
'''

# 委托：装饰器--哪些方法给哪个类调用，组合：把不同对象实例放在一个类中，继承：访问父类的方法

# 装饰器初步

'''
class tracer:
    def __init__(self,func):
        self.calls=0
        self.func=func

    def __call__(self, *args):
        self.calls += 1
        print('call {} to {}'.format(self.calls,self.func.__name__))

@tracer
def spam(a,b,c):
        print(a,b,c)

spam(1,2,3)
spam('a','b','c')
spam(4,5,6)

'''
'''
call 1 to spam
call 2 to spam
call 3 to spam
'''

'''
class X:
    a=1   #不能加self会变红
I=X()
X.a=2
print(I.a)  #2
J=X()
print(J.a)  #2
'''
'''
class C:
    shared=[]
    def __init__(self):
        self.perobj=[]

x=C()
y=C()
print(y.shared,y.perobj)
x.shared.append('spam')
x.perobj.append('spam')
print(x.shared,x.perobj)
print(y.shared,y.perobj)
print(C.shared)

'''
'''
[] []
['spam'] ['spam']
['spam'] []
['spam']
'''