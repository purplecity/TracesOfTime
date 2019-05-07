# 排序类型相同的对象，但是他们不支持原生的比较操作

# 跟operator.itemgetter()类似
# operator.attrgetter()就是干这个活的  不支持原生比较就用这个


class User:
    def __init__(self,user_id):
        self.user_id=user_id
    def __repr__(self):
        return 'User({})'.format(self.user_id)

users = [User(23), User(3), User(99)]
from operator import attrgetter
sorted(users,key=attrgetter('user_id'))  # [User(3), User(23), User(99)]

# 如果User有多个属性，可以多个参数排序
#by_name = sorted(users, key=attrgetter('last_name', 'first_name'))

#同样适用于min max
print(min(users, key=attrgetter('user_id')))

#User(3)
print(max(users, key=attrgetter('user_id')))
#User(99)