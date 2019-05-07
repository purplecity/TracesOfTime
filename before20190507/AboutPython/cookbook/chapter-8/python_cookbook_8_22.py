# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/15 12:10 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_22.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 栈和生成器替代递归

import types

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

class NodeVisitor:

    def visit(self,node):
        stack=[node]
        last_result=None
        while stack:
            try:
                last=stack[-1]
                if isinstance(last,types.GeneratorType):
                    stack.append(last.send(last_result))  #先发空值开始
                    print(len(stack),stack)
                    last_result=None  #一直发送的是None
                elif isinstance(last,Node):  #第一次就进入这里
                    stack.append(self._visit(stack.pop()))#这里是_visit返回的是一个生成器 meth(node)
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()

        return last_result

    #牛逼啊。   把生成器放到list里面还有这样的操作？？？、
    '''
    2 [<generator object Evaluator.visit_Add at 0x104597d00>, <__main__.Number object at 0x1045ed550>]
2 [<generator object Evaluator.visit_Add at 0x104597d00>, <__main__.Div object at 0x1045ed518>]
3 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <__main__.Mul object at 0x1045ed4a8>]
4 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, <__main__.Number object at 0x1045ed470>]
4 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, <__main__.Sub object at 0x1045ed438>]
5 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, <generator object Evaluator.visit_Sub at 0x1045df410>, <__main__.Number object at 0x1045ed3c8>]
5 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, <generator object Evaluator.visit_Sub at 0x1045df410>, <__main__.Number object at 0x1045ed400>]
5 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, <generator object Evaluator.visit_Sub at 0x1045df410>, -1]
4 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <generator object Evaluator.visit_Mul at 0x1045df3b8>, -2]
3 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, <__main__.Number object at 0x1045ed4e0>]
3 [<generator object Evaluator.visit_Add at 0x104597d00>, <generator object Evaluator.visit_Div at 0x1045df360>, -0.4]
2 [<generator object Evaluator.visit_Add at 0x104597d00>, 0.6]
0.6
    '''
    '''
        # 1 + 2*(3-4) / 5
    t1 = Sub(Number(3), Number(4))
    t2 = Mul(Number(2), t1)
    t3 = Div(t2, Number(5))
    t4 = Add(Number(1), t3)
    # Evaluate it
    e = Evaluator()
    print(e.visit(t4))

    1 t4是一个node。 pop t4经过_visit返回meth(t4) append 生成器函数visit_Add到stack中 长度为1
    2 对add  发送None send的返回值为yield的抛出值即Number(1) (注意并不是当做整体的两个yield相加。send一个就跳到下一个yield！！！) 增加到一个此时长度为2。。
    3 Number的是一个node。抛出并添加此时为add生成器对象和一个1 长度为2
    4 抛出1 lastresult=1 长度只有add了
    5 再次对add发送1。 从t4中断的地方继续执行此时t4(先接受1 ，级yield的右值yield Number(1) 成为1)  1+t3 抛出t3对象并添加。last_result=None  
    6 对t3 DIv 发送none 抛出t2 Mul. 此时长度为3 
    7 对t2 Mul发送None .抛出Number2 此时长度为4 
    8 是node  抛出Number2 添加2 长度为4
    9 抛出2  lastresult=2 长度为3
    10 再次对t2 Mul发送2  从t2中断的地方继续执行此时t2(先接受2 ，级yield的右值yield Number(2) 成为2)  抛出t1 lastresult=None 长度为4
    11 对t1 发送None 。t1开始。添加Number3. 暂停 长度为5  
    12 抛出Number3 -》 paochu 3 lasteresult=3  长度为4
    13 再次对t1 发送3. 从中断的地方继续执行此时t1(先接受3 即yield Number(3)的左值会变为3)3-yield Number(4） 抛出Number（4）暂停  长度为5 
    14 抛出Number4-》抛出4 lastresult=4 长度为4
    15 再次对t1 发送4 从中断的地方继续执行此时t1(先接受3 即yield Number(4)的左值会变为4)3-4）  t1 = -1  send的执行步骤没有yield了不能抛出报迭代错误。长度为4
    16 t1=-1 paochu  lastresult= -1
    17 再次对t2发出-1 从t2中断的地方继续执行此时t2(先接受-1 ，级yield的左值yield t1 成为-1)  t2=2*(-1)  end的执行步骤没有yield了不能抛出报迭代错误。长度为3
    18 t2=-2 paochu lastresult=-2
    19 对t3发送-2  从中断的地方继续执行此时t3(先接受-2 即yield t2)的左值会变为-2)  -2/yield Number(5） 抛出Number（5）暂停  长度为3
    20 抛出Number5 -》 paochu 5 lasteresult=5  长度为4
    21 对t3发送5  从中断的地方继续执行此时t3(先接受5 即yield Number(5)的左值会变为5)  -2/5 send的执行步骤没有yield了不能抛出报迭代错误 长度为3
    22 t3=-2/5 paochu  lastsulet= -2/5
    23 对t4发送-2/5 从中断的地方继续执行此时t3(先接受5 即yield t3的左值会变为5)  1-2/5 send的执行步骤没有yield了不能抛出报迭代错误 长度为2
    24 t4=-0.6 paochu  lastsulet=-2/5
    25 stack长度为0不再执行
    
    
    
    

    '''



    def _visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self,node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        yield (yield node.left) + (yield node.right)

    def visit_Sub(self, node):
        yield (yield node.left) - (yield node.right)

    def visit_Mul(self, node):
        yield (yield node.left) * (yield node.right)

    def visit_Div(self, node):
        yield (yield node.left) / (yield node.right)

    def visit_Negate(self, node):
        yield - (yield node.operand)

'''
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)
# Evaluate it
e = Evaluator()
print(e.visit(t4))  #<generator object Evaluator.visit_Add at 0x1044b5d00>  
#是一个生成器要么你用send 要么你就for。 而栈的那里就用了send
'''
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)
# Evaluate it
e = Evaluator()
print(e.visit(t4))

#讲真这些实例中不断包含实例的也是够恶心了.需要结合7-11看。


def gen():
    value=0
    while True:
        receive=yield value
        print(receive,value)
        if receive=='e':
            break
        value = 'got: %s' % receive

g=gen()
print(g.send(None))  # print(receive,value) 只为了让生成器开始执行receive等于None,value此时为0 # None 0
print(g.send('hello'))  #receive 先接受hello 此时value还是0，print(receive,value) hello 0  函数继续执行value 等于got: hello 。 抛出value被打印 暂停
print(g.send(123456)) #receive 接收123456 此时value还是got hello .print(receive,value) 123456 got:hello 函数继续执行到value等于got:123456 paochu value 被打印got:123456   暂停
print('hehe')
print(g.send('e')) #receive 接收e 此时value还是got 123456 .print(receive,value) e got:123456 break  没有再yiled了。所以报迭代错误。send的三个步骤执行不了了。

'''
hello 0
got: hello
123456 got: hello
got: 123456
hehe
e got: 123456
'''

#又巩固一遍对send的步骤的理解了。真他妈需要小心。这个stack 的循环搞虽然不是递归但也是有点绕弯需要仔细的