# 迭代遍历一个集合中元素的所有可能的排列或组合

items=['a','b','c']
# 排列 permutations  组合 combinantions

from itertools import  permutations,combinations
for p in permutations(items):  #可以选填第二个参数表示几个数的排列
    print(p)

print(items)
#同时使用会报错

'''
for x in combinations(items):
    print(x)

但是这样不报错

for x in combinations(items,2):
    print(x)
    
'''





# 看来连续使用迭代器的时候得小心
