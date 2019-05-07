#迭代器切片


#迭代器和生成器不能使用标准的切片操作，因为它们的长度事先我们并不知道(并且也没有实现索引)。 函数 islice() 返回一个可以生
# 成指定元素的迭代器，它通过遍历并丢弃直到
# 切片开始索引位置的所有元素。 然后才开始一个个
# 的返回元素，并直到切片结束索引位置。


def  count(n):
    while True:
        yield n
        n += 1
c= count(0)
#print(c[10:20])  # error

import itertools
for x in itertools.islice(c,10,20):
    print(x,end=' ')
    #10 11 12 13 14 15 16 17 18 19

for x in itertools.islice(c,2,20):
    print(x,end=' ')

    #22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39

#这里要着重强调的一点是 islice() 会消耗掉传入的迭代器中的数据。 必须考虑到迭代器是
# 不可逆的这个事实。 所以如果你需要之后再次访问这个迭代器的话，那你就得先将它里面的数
# 据放入一个列表中。这里就把20以前的数都切掉了
