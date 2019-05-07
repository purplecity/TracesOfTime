# 带有外部状态的生成器函数

from collections import  deque
class linehistory:
    def __init__(self,lines,histlen=3):
        self.lines=lines
        self.history=deque(maxlen=histlen)

    def __iter__(self):
        for lineno,line in enumerate(self.lines,1):   #第二个参数，起始位置
            self.history.append((lineno,line))
            yield  line
    def clear(self):
        self.history.clear()

with open('/Users/purplecity/a.txt') as f:
    lines=linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno,hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')

# 把出现python之前的前三行打印出来

'''
a.txt 

pythonhello world
python2
hehe
python3
letgo
python4


1:pythonhello world
1:pythonhello world
2:python2
2:python2
3:hehe
4:python3
4:python3
5:letgo
6:python4


关于生成器，很容易掉进函数无所不能的陷阱。 如果生成器函数
需要跟你的程序其他部分打交道的话(比如暴露属性值，允许通
过方法调用来控制等等)， 可能会导致你的代码异常的复杂。 如
果是这种情况的话，可以考虑使用上面介绍的定义类的方式。 
在 __iter__() 方法中定义你的生成器不会改变你任何的算法
逻辑。 由于它是类的一部分，所以允许你定义各种属性和方法
来供用户使用。


'''
