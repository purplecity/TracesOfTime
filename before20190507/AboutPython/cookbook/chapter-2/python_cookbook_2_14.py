# 合并拼接字符串

# 合并的字符串是在一个序列或者 iterable 中，那么最快的方式就是使用 join() 方法

'''
    def join(self, iterable): # real signature unknown; restored from __doc__
        """
        S.join(iterable) -> str

        Return a string which is the concatenation of the strings in the
        iterable.  The separator between elements is S.
        """
        return ""

        列表，元组，字典，文件，集合或生成器

'''


parts = ['Is', 'Chicago', 'Not', 'Chicago?']
print(' '.join(parts))
print(','.join(parts))
print(''.join(parts))
data=['ACME', 50, 91.1]
print(','.join(str(d) for d in data))


def sample():
    yield  'Is'
    yield  'Chicago'
    yield  'Not'
    yield  'Chicago'

test=''.join(sample())
print(test)


#把source中每一行叠加成一个字符串片段，当长度超过maxsize。就开始下一个叠加字符串片段。
def combine(source,maxsize):
    parts=[]
    size=0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield  ''.join(parts)
            parts=[]
            size=0
    yield ''.join(parts) #把剩下的也连起来

with open('filename','w') as f:
    for part in compile(sample(),32768):
        f.write(part)






