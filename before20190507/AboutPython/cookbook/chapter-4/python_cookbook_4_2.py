# 构建了一个自定义容器对象，里面包含有列表、元组或其他可迭代对象。 你想直接在你的这个新容器对象上执行迭代操作，将迭代操作代理到容器内部的对象上去

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


# list元素可以是类的实例....for的本质是调用__iter__方法返回一个迭代器，这里交给内置函数去返回。作用于类中的属性上
# 真是意犹未尽...
'''
Node(1)
Node(2)

'''