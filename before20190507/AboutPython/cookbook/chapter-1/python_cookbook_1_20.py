# 合并字典

from collections import ChainMap

a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }

''''''
x=b.update(a)  # 这样操作不行
print(type(x))  #NoneType


h=dict(b)
h.update(a)
print(type(h))
print(h['x'])
a['x']=13
print(h['x'])

merged=ChainMap(a,b)
print(merged['x'])
a['x']=42
print(merged['x'])

'''
原字典做了更新，这种改变不会反应到新的合并字典中去
ChainMap 使用原来的字典，它自己不创建新的字典

一个 ChainMap 接受多个字典并将它们在逻辑上变为一个字典。 然后，这些字典并不是真的合并在一起了， ChainMap 类只是在内部创建了一个容纳这些字典的列表 并重新定义了一些常见的字典操作来遍历这个列表。大部分字典操作都是可以正常使用的



'''
print(len(merged))
print(list(merged.keys()))
print(list(merged.values()))

#对于ChainMap字典的更新或删除操作总是影响的是列表中第一个字典。比如：
merged['z']=10
print(merged)
merged['w']=40
print(merged)
del merged['x']
print(merged)
# del  merged['y']不能操作出第一个外的删除或者更新操作

'''
<class 'NoneType'>
<class 'dict'>
1
1
13
42
3
['x', 'z', 'y']
[42, 3, 2]
ChainMap({'x': 42, 'z': 10}, {'y': 2, 'z': 3, 'x': 1})
ChainMap({'x': 42, 'z': 10, 'w': 40}, {'y': 2, 'z': 3, 'x': 1})
ChainMap({'z': 10, 'w': 40}, {'y': 2, 'z': 3, 'x': 1})

'''