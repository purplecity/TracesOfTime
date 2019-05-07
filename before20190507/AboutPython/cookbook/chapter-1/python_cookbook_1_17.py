# 构造一个字典，是另外一个字典的子集

prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

p1={key:value for key,value in prices.items() if value > 200 }
# key:value 是最外面的元素，然后key value 遍历。判断
# items返回的是一个元组！！！

tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2={key:value for key,value in prices.items() if key in tech_names}

# 字典推导，list推导等等。就是在 符号 元素  for 判断的格式


#强行转换 把tuple转化为dict的一个元素。这种方法运行慢一倍

p3=dict(  (key,value) for key,value in prices.items() if value > 200    )

#下面这种慢1.6倍。
p4={key:prices[key] for key in prices.keys() & tech_names }

