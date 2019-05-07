# /Users/purplecity




# 在迭代操作或者其他操作的时候，怎样只保留最后有限几个元素的历史记录 通过deque的maxlen最老删除这个特性


from collections import deque

def search(lines,pattern,history=5):
    previous_lines=deque(maxlen=history)   #deque是一个双向列表。这里的是设置最大长度为5.如果超出最大值，最老的元素会被抛出
    for line in lines:
        if pattern in line:
            yield line,previous_lines
            #previous_lines.append(line)  和下面是两行不同的结果
        previous_lines.append(line)

if __name__=='__main__':
    with open(r'/Users/purplecity/a.txt') as f:
        for line,prevlines in search(f,'python',5):
            for pline in prevlines:
                print(pline,end='')  #end=''的作用是不打印换行符。如果这里没有end=''会换行
            print(line,end='')
            print('_'*20)

'''
生成器generator补充

生成器保存的是算法。

第一种方法就是改列表生成式的[]为()

L = [x * x for x in range(10)]   列表生成式直接创建一个列表。占用空间
g = (x * x for x in range(10))  <generator object <genexpr> at 0x1022ef630>

next(g)不断打印值（0,1,4,9....）。直到没有更多元素抛出报错。
for 循环不断打印纸。且不必担心错误。
for n in g:
    print n
    
    
第二种方法就是生成器函数。有yield关键字的就是生成器函数。yield:英语是生成的意思
生成器保存的是算法
同样可以采用next和for循环print



def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

    
o = odd()
next(o) （1,3,5）直到报错
for循环打印不必报错
for n in o:
    print n

generator函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。    
    
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
    
f = fib(6)
f 类型 <generator object fib at 0x104feaaa0>

>>> for n in fib(6):
...     print(n)

#  1 1 2 3 5 8
    

'''
