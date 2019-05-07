prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

################## zip()反转键值
m=zip(prices.values(),prices.keys())
a=prices.values()
b=prices.keys()
print(type(a),type(b))   #<class 'dict_values'> <class 'dict_keys'>  并不是一个list类型,但是可用泛型遍历取出所有key值
print(prices.values(),prices.keys())  #dict_values([45.23, 612.78, 205.55, 37.2, 10.75]) dict_keys(['ACME', 'AAPL', 'IBM', 'HPQ', 'FB'])
print(type(prices.values()),type(prices.keys()))  #<class 'dict_values'> <class 'dict_keys'>
print(list(m))  #[(45.23, 'ACME'), (612.78, 'AAPL'), (205.55, 'IBM'), (37.2, 'HPQ'), (10.75, 'FB')]
#可以见到zip() 函数方案通过将字典”反转”为 (值，键) 成   元组序列。元组比的大小是跟字符串一样逐个比的，所以有：

min_price = min(zip(prices.values(), prices.keys()))
# min_price is (10.75, 'FB')
max_price = max(zip(prices.values(), prices.keys()))
# max_price is (612.78, 'AAPL')
print(min_price,max_price)

prices_sorted = sorted(zip(prices.values(), prices.keys()))
# prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
#                   (45.23, 'ACME'), (205.55, 'IBM'),
#                   (612.78, 'AAPL')]
# sorted返回的是一个list

#需要注意的是 zip() 函数创建的是一个只能访问一次的迭代器。 比如，下面的代码就会产生错误：
prices_and_names = zip(prices.values(), prices.keys())
print(min(prices_and_names)) # OK
print(max(prices_and_names)) # ValueError: max() arg is an empty sequence

print(type(m))  # <class 'zip'>


# 跟以下认知有点冲突
'''
python zip（）和zip（*）的区别
可以看成是解压和压缩的区别，zip相当与压缩  zip（*）相当于解压。

x=["a","1"]
y=["b","2"]
z = list(zip(x,y))
print (list(zip(x,y)))
print (list(zip(*z)))

结果为：

[('a', 'b'), ('1', '2')]

[('a', '1'), ('b', '2')]

zip的内容要经过list之后才能显示出来。

'''


###############单纯的作用于dict

# 起作用的是键不是值
min(prices) # Returns 'AAPL'
max(prices) # Returns 'IBM'
min(prices.values()) # Returns 10.75
max(prices.values()) # Returns 612.78

#min() 和 max() 函数中提供 key 函数参数来获取最小值或最大值对应的键的信息
# 感叹这个key参数真是给力好几次见到其他场合了
min(prices, key=lambda k: prices[k]) # Returns 'FB'
max(prices, key=lambda k: prices[k]) # Returns 'AAPL'

min_value = prices[min(prices, key=lambda k: prices[k])]



