# 实现迭代器协议   4-2其实已经实现了

#关键意思：实现迭代器协议用生成器函数简单的多。强行写next方法并不讨好

#回顾4.1
# 理解迭代协议  Python 迭代协议要求一个 __iter__() 方法返回一个特殊的迭代器，这个迭代器实现了 __next__()　方法，并通过 StopIteration异常标识迭代完成。


class Node:
    def __init__(self,value):
        self._value=value
        self._children=[]

    def __repr__(self):
        return '({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield  self
        for c in self:   #调用的__iter__
            yield  from c.depth_first()

if __name__=='__main__':
    root=Node(0)
    child1=Node(1)
    child2=Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)

#  返回自己本身并迭代每一个子节点并 通过调用子节点的 depth_first() 方法(使用 yield from 语句)返回对应元素

# 意犹未尽...

'''

(0)
(1)
(3)
(4)
(2)
(5)
'''


'''
对比下4-2


class Node:
    def __init__(self,value):
        self._value=value
        self._children=[]

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self,node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)


if __name__=='__main__':
    root=Node(0)
    child1=Node(1)
    child2=Node(2)
    root.add_child(child1)
    root.add_child(child2)

    for ch in root:
        print(ch)

'''

