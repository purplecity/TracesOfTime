# 序列化python对象  pickle

#将一个Python对象序列化为一个字节流，以便将它保存到一个文件、存储到数据库或者通过网络传输它。

# dumps 对象->字符串 loads 字符串->对象 只有一个参数
# dump(data,f)  把data保存在f中 data=load(f) 恢复对象

'''
import pickle

data=...
f=open('somefile','wb')
pickle.dump(data,f)
s=pickle.dumps(data)

#from a file
f=open('somefile','rb')
data=pickle.load(f)

#from a str
data=pickle.loads(s)
'''

# 记录对象开始结尾信息，逐个load
#pickle 是一种Python特有的自描述的数据编码。 通过自描述，被序列化
# 后的数据包含每个对象开始和结束以及它的类型信息。 因此，你无需担心对
# 象记录的定义，它总是能工作。 举个例子，如果要处理多个对象，你可以
# 这样做：


'''

>>> import pickle
>>> f = open('somedata', 'wb')
>>> pickle.dump([1, 2, 3, 4], f)
>>> pickle.dump('hello', f)
>>> pickle.dump({'Apple', 'Pear', 'Banana'}, f)
>>> f.close()
>>> f = open('somedata', 'rb')
>>> pickle.load(f)
[1, 2, 3, 4]
>>> pickle.load(f)
'hello'
>>> pickle.load(f)
{'Apple', 'Pear', 'Banana'}
>>>

'''

#一般都是json格式，这个只做了解就好
'''

有些类型的对象是不能被序列化的。这些通常是那些依赖外部系统状态的对象， 比如打开的文件，网络连接，线程，
进程，栈帧等等。 用户自定义类可以通过提供 __getstate__() 和
 __setstate__() 方法来绕过这些限制。 如果定义了这两个方法，
 pickle.dump() 就会调用 __getstate__() 获取序列化的对象。
  类似的，__setstate__() 在反序列化时被调用。为了演示这个工作原理，
   下面是一个在内部定义了一个线程但仍然可以序列化和反序列化的类：
'''

import time
import threading

class Countdown:
    def __init__(self,n):
        self.n=n
        self.thr=threading.Thread(target=self.run)
        self.thr.daemon=True
        self.thr.start()

    def run(self):
        while self.n>0:
            print('T-minus',self.n)
            self.n -= 1
            time.sleep(5)
    def __getstate__(self):
        return self.n

    def __setstate__(self, n):
        self.__init__(n)

