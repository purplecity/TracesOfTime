# 代码从下标操作中解脱出来
# 下标访问->名称访问的


#基础知识
# namedtuple返回元组的别名。就相当于结构体

from collections import namedtuple

#1 定义一个nametuple类型，包含属性
Use=namedtuple('User',['name','sex','age'])
# 实例化
user=Use(name='koo',sex='male',age='21')

print (user.name) # koo
print (user.age) #male
print(user.sex) # 21
print(type(user),user)  #<class '__main__.User'> User(name='koo', sex='male', age='21')

#具有所有元组的方法，比如索引和解压
print(len(user))
name,sex,age=user
print(name,sex,age)

# 3
# koo male 21


####解脱下标
def compute_cost(records):
    total=0.0
    for rec in records:
        total +=rec[1]*rec[2]
    return total

Stockhaha=namedtuple('Stock',['name','shares','price'])
def compute_cost_2(records):
    total=0.0
    for rec in records:
        s=Stockhaha(*rec)
        total += s.shares*s.price
    return total


#命名元组不可更改。如果要更改要用_replace()方法，会创建一个全新的命名元组并将对应的字段用新的值取代

Stock = namedtuple('Stockee', ['name', 'shares', 'price', 'date', 'time'])
instance_moren=Stock('',0,0.0,None,None)
def dict_to_stock(s):
    return instance_moren._replace(**s)

a = {'name': 'ACME', 'shares': 100, 'price': 123.45}

b = {'name': 'ACME', 'shares': 100, 'price': 123.45, 'date': '12/17/2012'}

print(dict_to_stock(a),dict_to_stock(b))
#Stockee(name='ACME', shares=100, price=123.45, date=None, time=None) Stockee(name='ACME', shares=100, price=123.45, date='12/17/2012', time=None)




