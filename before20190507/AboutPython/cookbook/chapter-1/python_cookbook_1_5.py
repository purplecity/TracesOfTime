#  heap知识。

'''
可以通过 list 对 heap 进行初始化，或者通过 api 中的 heapify 将已知的 list 转化为 heap 对象。

heapq.heapify(x)：Transform list into a heap, in-place, in O(len(x)) time
heapq.heappush(heap, item)

这两个能构造一个堆。前者是转化为heap对象。后者是构造堆。


堆数据结构最重要的特征是 heap[0] 永远是最小的元素。并且剩余的元素可以很容易的通过调用 heapq.heappop() 方法得到， 该方法会先将第一个元素弹出来







'''

# 用heap模块实现简单的优先级队列。关键是  1  push可以push的是一个元组  2 元组之间可以比较。类似于字符串的比较，从第一个元素开始
# 比较。如果两个类型不相同，要进行相应的转换，而且数字元素最小。


import heapq

class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0

    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index += 1 #保证优先级相同的元素  保持着 先进先出的 队列模型

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q=PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)

q.pop() #执行4次，分别是值是  Item('bar') Item('spam') Item('foo') Item('grok')

