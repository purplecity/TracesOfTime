#######  字典的交并差！！！
'''
集合有交并差运算。 对应于& | -符号
dict是键值对集合,试了没有|-&运算，用items替代
keys是一个key集合。有|-&运算
'''


a = {
    'x' : 1,
    'y' : 2,
    'z' : 3
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}
#print(a |-& b)
print(a.keys() | b.keys())  # {'y', 'w', 'z', 'x'}
print(type(a.keys()))  #<class 'dict_keys'>
print(type(a.keys() | b.keys() )) # <class 'set'>
print(type(a.items()))  #<class 'dict_items'>

print(a.items() | b.items())  #{('z', 3), ('y', 2), ('w', 10), ('x', 1), ('x', 11)}
print(type(a.items()| b.items()))  #<class 'set'>



###########常用写法
c = {key:a[key] for key in a.keys() - {'z', 'w'}}
# c is {'x': 1, 'y': 2}
# key:a[key]是外面符号{}的元素，key是遍历变量










