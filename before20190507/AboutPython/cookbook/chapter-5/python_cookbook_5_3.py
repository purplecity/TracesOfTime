# 想使用print()函数输出数据，但是想改变默认的分隔符或者行尾符

print('nice',40,51.5)
print('nice',40,51.5,sep=',')
print('nice',40,51.5,sep=',',end='!!\n')

for i in range(5):
    print(i)

for x in range(5):
    print(x,end='   ')


print(','.join('nice','40','51.5'))
#只是用与字符串。类型不同需要转字符串。如下
row = ('ACME', 50, 91.5)
print(','.join(str(x) for x in row))



'''
nice 40 51.5
nice,40,51.5
nice,40,51.5!!
0
1
2
3
4
0   1   2   3   4   

'''