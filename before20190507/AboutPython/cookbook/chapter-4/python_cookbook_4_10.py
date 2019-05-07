# enumerate的更多使用

#将一个文件中出现的单词映射到它出现的行号上去

from collections import defaultdict

word_summary=defaultdict(list)
with open('/Users/purplecity/a.txt','r') as f:
    lines = f.readlines()

for idx,line in enumerate(lines):
    words=[w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)

print(word_summary)

#如果某个单词在一行中出现过两次，那么这个行号也会出现两次

'''

a.txt
python hello world
python hello my gold
hehe maybe world
python yes it is
letgo honor
python letgo

defaultdict(<class 'list'>, {'python': [0, 1, 3, 5], 'hello': [0, 1], 'world': [0, 2], 'my': [1], 'gold': [1], 'hehe': [2], 'maybe': [2], 'yes': [3], 'it': [3], 'is': [3], 'letgo': [4, 5], 'honor': [4]})


'''