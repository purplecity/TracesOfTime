# counter类

''''
class Counter(dict):
继承于dict

def __init__(*args, **kwds):
    Create a new, empty Counter object.  And if given, count elements
    from an input iterable.  Or, initialize the count from another mapping
    of elements to their counts.

    >>> c = Counter()                           # a new, empty counter
    >>> c = Counter('gallahad')                 # a new counter from an iterable
    >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
    >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

'''

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

from collections import Counter

word_counts=Counter(words)
print(type(word_counts))   #<class 'collections.Counter'>
print(word_counts['not'],word_counts['eyes'])  #1 8  在底层实现上，一个 Counter 对象就是一个字典，将元素映射到它出现的次数上
top_three=word_counts.most_common(3)
print(type(top_three),top_three)  #<class 'list'> [('eyes', 8), ('the', 5), ('look', 4)]

#在此基础上手动增加计数
morewords = ['why','are','you','not','looking','in','my','eyes']
for word in morewords:
    word_counts[word] += 1
print(word_counts['eyes'])  #9

#直接更新update方法
word_counts.update(morewords)

'''
def update(*args, **kwds):
    Like dict.update() but add counts instead of replacing them.

    Source can be an iterable, a dictionary, or another Counter instance.

    >>> c = Counter('which')
    >>> c.update('witch')           # add elements from another iterable
    >>> d = Counter('watch')
    >>> c.update(d)                 # add elements from another counter
    >>> c['h']                      # four 'h' in which, witch, and watch
    

    
    # The regular dict.update() operation makes no sense here because the
    # replace behavior results in the some of original untouched counts
    # being mixed-in with all of the other counts for a mismash that
    # doesn't have a straight-forward interpretation in most counting
    # contexts.  Instead, we implement straight-addition.  Both the inputs
    # and outputs are allowed to contain zero and negative counts.
'''

x=Counter(words)
y=Counter(morewords)
print(x,y)
#  Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1}) Counter({'why': 1, 'are': 1, 'you': 1, 'not': 1, 'looking': 1, 'in': 1, 'my': 1, 'eyes': 1})
#

print(x+y)
# Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2,
# 'around': 2, "you're": 1, "don't": 1, 'in': 1, 'why': 1,
# 'looking': 1, 'are': 1, 'under': 1, 'you': 1})
print(x-y)

# Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2,
# "you're": 1, "don't": 1, 'under': 1})


'''
其他
    Dict subclass for counting hashable items.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> c = Counter('abcdeabcdabcaba')  # count elements from a string

    >>> c.most_common(3)                # three most common elements
    [('a', 5), ('b', 4), ('c', 3)]
    >>> sorted(c)                       # list all unique elements
    ['a', 'b', 'c', 'd', 'e']
    >>> ''.join(sorted(c.elements()))   # list elements with repetitions
    'aaaaabbbbcccdde'
    >>> sum(c.values())                 # total of all counts
    15

    >>> c['a']                          # count of letter 'a'
    5
    >>> for elem in 'shazam':           # update counts from an iterable
    ...     c[elem] += 1                # by adding 1 to each element's count
    >>> c['a']                          # now there are seven 'a'
    7
    >>> del c['b']                      # remove all 'b'
    >>> c['b']                          # now there are zero 'b'
    0

    >>> d = Counter('simsalabim')       # make another counter
    >>> c.update(d)                     # add in the second counter
    >>> c['a']                          # now there are nine 'a'
    9

    >>> c.clear()                       # empty the counter
    >>> c
    Counter()

    Note:  If a count is set to zero or reduced to zero, it will remain
    in the counter until the entry is deleted or the counter is cleared:

    >>> c = Counter('aaabbc')
    >>> c['b'] -= 2                     # reduce the count of 'b' by two
    >>> c.most_common()                 # 'b' is still in, but its count is zero
    [('a', 3), ('c', 1), ('b', 0)]
'''