##### 删除序列相同元素并保持顺序
'''
hashable和unhashable

如果一个对象在其生命周期内有一个固定不变的哈希值 (这需要__hash__()方法) 且可以与其他对象进行比较操作 (这需要__eq__()方法) ，那么这个对象就是可哈希对象 (hashable) 。可哈希对象必须有相同的哈希值才算作相等。
由于字典 (dict) 的键 (key) 和集合 (set) 内部使用到了哈希值，所以只有可哈希 (hashable) 对象才能被用作字典的键和集合的元素。可哈希对象和不可哈希对象的区别体现在：可哈希对象可以作为字典的键和集合的元素，不可哈希对象则不可以。

'''

a = [1, 5, 2, 1, 9, 1, 5, 10]
set(a)  #{1, 2, 10, 5, 9}虽然删除了单没有保持顺序

# 如果序列上的值都是 hashable 类型，那么可以很简单的利用集合或者生成器来解决这个问题
def dedupe(items):
    seen=set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

# 生成器函数通过next获得值，可以直接list出来。要想获得返回值要循环next并且捕获异常才行。所以这里return没意义

list(dedupe(a))  #  [1, 5, 2, 9, 10]


# 如果想消除元素不可哈希（比如 dict 类型）的序列中重复元素的需要改变一下
def dedupe(items,key=None):
    seen=set()
    for item in items:
        val=item if key is None else key(item)
        if val not in seen:
            yield item  #判断的是val，返回的是item！
            seen.add(val)


'''
元组相等是所有元素相等
>>> a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
>>> list(dedupe(a, key=lambda d: (d['x'],d['y'])))
[{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
>>> list(dedupe(a, key=lambda d: d['x']))
[{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
>>>


# 应用：读取一个文件，消除重复行



with open(somefile,'r') as f:
for line in dedupe(f):
    print(line)
    
'''
