# 解压一个可迭代对象的N个元素出来。用*号表达式。前中后都可以。类型自己加type判断
# eg:
#  record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
#  (*)name, (*)email, (*)phone_numbers = record  前中后任意一个
#  print(type(phone_numbers))  list



# 在可变长元素的序列中的*号使用
records=[
    ('foo',1,2),
    ('bar','hello'),
    ('foo',3,4)
]

def do_foo(x,y):
    print('foo',x,y)

def do_bar(s):
    print('bar',s)

for tag,*args in records: # 1 args可变长 2 我以前都是整体遍历的，如for x in records:
    if tag=='foo':
        do_foo(*args)
    elif tag=='bar':  #elif后面没有else了
        do_bar(*args)

# 字符串的使用
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname,*fields,homedir,sh=line.split(':')
print(uname,homedir) # 'nobody','/var/empty'

record = ('ACME', 50, 123.45, (12, 18, 2012))
name,*_,(*_,year)=record
print(name,year) #'ACME',2012


#递归
items = [1, 10, 7, 4, 5, 9]
def sum(items):
    head,*tail=items
    return head+sum(tail) if tail else head  #如果tail为真就返回head+sum(tail),否则返回head

sum(items) #36



