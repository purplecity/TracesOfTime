# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/8 4:47 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_12.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


# 你想定义一个接口或抽象类，并且通过执行类型检查来确保子类实现了某些特定的方法
# 暂时感觉用不到...

from abc import ABCMeta,abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self,maxbytes=-1):
        pass

    @abstractmethod
    def write(self,data):
        pass

class SocketStream(IStream):
    def read(self,maxbytes=-1): pass

    def write(self,date): pass

def serialize(obj,stream):
    if not isinstance(stream,IStream):
        raise TypeError('Expected an IStream')
    pass