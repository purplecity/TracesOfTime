# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/7 9:33 PM                               
#  Author           purplecity                                       
#  Name             python风格纸牌.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import collections

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list("JQKA")
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank,suit) for suit in self.suits
                                      for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]

from random import choice

a = choice(FrenchDeck())
print(a)

suit_values = dict(spades=3,hearts=2,diamonds=1,clubs=0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(FrenchDeck(),key=spades_high):
    print(card)

# 一个类的实例表现的像python自有的数据类型一样。这就是len和getitem这些特殊方法的方法的用处。


# 实现一个可以+ - 的n维类

from math import hypot

class Vector:

    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector({},{})'.format(self.x,self.y)

    def __abs__(self):
        return hypot(self.x,self.y)

    def __bool__(self):
        return bool(self.x or self.y)

    def __add__(self,other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)

    def __mul__(self, other):
        return Vector(self.x * other,self.y * other)


# 默认情况下，我们自己定义的类的实例总被认为是真的，除非这个类对
# __bool__ 或者 __len__ 函数有自己的实现。bool(x) 的背后是调用
# x.__bool__() 的结果；如果不存在 __bool__ 方法，那么 bool(x) 会
# 尝试调用 x.__len__()。若返回 0，则 bool 会返回 False；否则返回
# True。