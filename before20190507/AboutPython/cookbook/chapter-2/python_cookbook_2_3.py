# 类似于shell匹配模式来匹配字符串

# 用到两个函数，fnmatch fnmatchcase，参数都是匹配对象和匹配模式
# 后者严格区分大小写。前者因操作系统不同不严格匹配大小写

from fnmatch import fnmatch,fnmatchcase
print(fnmatch('foo.txt','*.txt'))  # True
print(fnmatch('foo.txt','?oo.txt'))  # True
print(fnmatch('Dat45.csv','Dat[0-9]*')) #True

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([ name for name in names if fnmatch(name,'Dat*.csv')])
# ['Dat1.csv', 'Dat2.csv']

addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]

print([ addr for addr in addresses if fnmatchcase(addr,'*.ST')])

