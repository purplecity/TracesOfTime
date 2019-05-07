# 字典映射多个值。

'''
d = {
    'a' : [1, 2, 3],
    'b' : [4, 5]
}
e = {
    'a' : {1, 2, 3},
    'b' : {4, 5}
}
'''

#key的field是一个list或者set


from collections import defaultdict


'''
    def __init__(self, seq=None, **kwargs): # known special case of dict.__init__
        """
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """
        pass
'''

d=defaultdict(list)
print(type(d['a']))  #list
d['a'].append(1)
d['a'].append(2)
d['b'].append(3)

d=defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(3)

x={}
x['a'].append(2)
y={}
y['b'].add(3)
#这两行居然可以通过。毕竟默认field就可以是list和set所以可以调用方法 那敢情创建多值字典不用defaultdict？？？
# 错。关键是dict访问一个不存在的key会错。而defauldict不会而且可以操作！
# 所以之前的list或者set参数的意思就是固定了field的类型！！！！！ 怪不得参数为list的时候不能调add方法

'''

d={}
for key,value in pairs:
    if key not ind d：
        d[key]=[]
    d[key].append(value)
    
d=defaultdict(list)
for key,value in pairs:
    d[key].append(value)
'''


# defaultdict 的一个特征是它会自动初始化每个 key 刚开始对应的值
# defaultdict 会自动为将要访问的键（就算目前字典中并不存在这样的键）创建映射实体。普通的dict访问一个不存在的key会报错。
# dict.setdefault()方法接收两个参数，第一个参数是健的名称，第二个参数是默认值。假如字典中不存在给定的键，则返回参数中提供的默认值；反之，则返回字典中保存的值。

d={}
d.setdefault('a',[]).append(1)
d.setdefault('a',[]).append(2)

d.setdefault('b',{[]}).add(3)
# 要创建一个set，需要提供一个list作为输入集合
'''
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}
'''















