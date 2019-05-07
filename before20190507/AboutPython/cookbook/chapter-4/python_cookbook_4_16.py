#迭代器代替while无限循环

#iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记(结尾)值作为输入参数。 当以这种方式
# 使用的时候，它会创建一个迭代器， 这个迭代器会不断调用 callable 对象直到返回值和标记值相等为止。
#iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记(结尾)值作为输入参数。 当以这种方式使用的时候，它会创建一个迭代器， 这个迭代器会不断调用 callable 对象直到返回值和标记值相等为止。

#这种特殊的方法对于一些特定的会被重复调用的函数很有效果，比如涉及到I/O调用的函数。 举例来讲，如果你想从套接字或文件中以数据块的方式读取数据，通常你得要不断重复的执行 read() 或 recv() ， 并在后面紧跟一个文件结尾测试来决定是否终止。这节中的方案使用一个简单的 iter() 调用就可以将两者结合起来了。 其中 lambda
#函数参数是为了创建一个无参的 callable 对象，并为 recv 或 read() 方法提供了 size 参数。

import sys
f=open('/etc/passwd')
for chuck in iter(lambda: f.read(10),''):  #直到为空截止。连换行符也读进去了。 返回的是表达式的值。
    n=sys.stdout.write(chuck)
