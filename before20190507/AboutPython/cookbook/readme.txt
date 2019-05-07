
python_cookbook_1_8 zip反转键值  跟zip本身意义不对。原理不明
--------------------------------
python_cookbook_2_15 __missing__这个方法被提及。

Maybe:

class Missing(dict):
    def __missing__(self, key):
        return 'missing'

d=Missing()
print(d['hehe'])  #missing

format中逗号千位分隔符,貌似会丢失一定小数位数。
print('{:,}'.format(9987733498273.0432)) #9,987,733,498,273.043
print('{:,}'.format(987733498273.0432)) #987,733,498,273.0432
print('{:,}'.format(87733498273.04325))   #87,733,498,273.04324
print('{:,}'.format(987733498273.04325)) #987,733,498,273.0432
print('{:,}'.format(733498273.04325666)) #733,498,273.0432566

Maybe:
其实就是浮点数的精度17位是最大值了。


-------------------------------------------------------
2_18 2_19 2_20全pass 就是字节编码，正则表达式没看。2-18令牌流不知道啥意思
------------------------------------------------------------------------
3-9    can't find reference 'array' in  __init__ 使用numpy的array方法时变黄
Maybe:
pycharm的bug

----------------------------------------------------------

4-16   lambda  创建一个可回调对象，执行表达式，返回表达式的值？
------------------------------------------------------------

5-21   pcikle一个线程对象的时候，重写__getstate__ __setstate__之后，
线程是啥时候终止又是怎么的内部原理让线程恢复，f.close也能导致正在序列化的线程挂了吗
感觉pickle用处不大啊。

----------------------------------------------------
6-12  装饰器元类  setaddr getaddr __get__ __set__以及为啥f = open('polys.bin', 'rb')
>>> phead = PolyHeader(f.read(40)) 这里并没有说内存。为啥就可以直接访问属性直接解包了呢。 很不明白

----------------------------------------------------------------------
元类 装饰器 __xx__方法是一个痛点  看了这张搞个专题。python学习手册解决这个痛点再来看在这个问题
---------------------------------------------------------------------
property居然可以添加方法为啥
class newprops(object):
    def getage(self):
        return 40  # 相当于 def getage(self): return _age  只不过_age=40 参照propertiy的初始化
    def setage(self,value):
        print('set age:',value)
        self._age=value

    age=property(getage,setage,None,None)

x=newprops()
# print(x.hehe)  报错没有hehe
print(x.age)  #
x.age=42
print(x._age)  #把age的值给_age
x.job='trainer'  # job又是一个property?
print(x.job)  #真不太清楚为啥 job这里没有调用getage  又遇到一个python学习手册P1098
print(list(getattr(x,'__dict__')))   ！！！！！！！！！！！！！！！！！！！  #['_age', 'job'] 真神奇
---------------------------------------------
python学习手册p1034 装饰器和描述器结合那个代码那还没搞明白
----------------------------------
autobahn那个库。 protocol中的websocketClientFactory既没显示继承interface中的channelFactory也没有regist为虚拟子类，难道实现了全部抽象方法就默认是子类了吗
-----------------------------------------------------
https://docs.python.org/3/library/asyncio-protocol.html两个例子看不太懂
----------------------------------------------
7-11中 funtion.wraps为啥能保持自己的原函数属性不知道啥原因
-----------------------------------------------------
8-10  dir(c)为啥会有这几个属性，这几个没有self啊。应该不是属于实例或者类的属性啊。'area', 'perimeter' 。解答:因为dir包括所有的函数方法和不是self的变量。是可以直接调用的
-------------------------------------------------------------------------
8-13 装饰器Typed中为啥当cls is None的时候会return lmbda cls: Typed(expected_type,cls)？？？？这不是死循环吗。。。
--------------------------------------------
9-5  这里不是死循环了吗 return partial(attach_wrapper,obj)
----------------------------------------
9-9  #  print(s.bar.ncalls)   print(s.bar,type(s.bar))  #<bound method Spam.bar of <__main__.Spam object at 0x106baa4a8>> <class 'method'>这两个跟最后分析的调用ncalls解释不合理
实例调用参数 应该是调用__call__ 然后传参。

-------------------------
9-13
# aaa 是真的服气。
# 1元类的call怎么调用。难道真如所说？https://www.cnblogs.com/huchong/p/8260151.html  2  self.__instance=super().__call__(*args,**kwargs) 如果是super往mro后搜索，1为啥不管是为啥还有super会有call方法2init的返回是一个类这里为啥返回一个实例3返回实例居然还打印了print('creating spam')？？？ super跟call啥关系？

-----------------------
return types.MethodType(self,instance)  self instance 都是类这有啥用
----------------------------------------------------
12-6 同一个conn实例。被两个线程使用，结果还没个线程创建一个自己专属的套接字连接  还真是这样操作的。local实例是全局的。每个线程都可以使用这个实例。然后自己添加东西？
看定义是的。threading.local的实例为每个线程维护一个单独的实例字典。  是一个实例为每个线程  维护一个单独的字典。  每个线程的字典都由threading.local维护。
-------------------------
12-12  网络例子还没看明白
---------
