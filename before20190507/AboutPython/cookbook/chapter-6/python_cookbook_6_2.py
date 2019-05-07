# 第六章在于获取和保存数据。平常转换的是json数据。以后再说
# 第六章估计不会太多。

import json

'''
data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
}

with open('data.json','w') as f:
    json.dump(data,f)


with open('data.json','r') as f:
    data=json.load(f)
'''
print(json.dumps(False))
d={'a':True,'b':'Hello','C':None}
print(json.dumps(d))
'''
关键词的转换

false
{"a": true, "b": "Hello", "C": null}
'''

'''
当数据的嵌套结构层次很深或者包含大量的字段时。 为了解决这个问题，可以考虑使用pprint模块的 pprint() 函数来代替普
通的 print() 函数。 它会按照key的字母顺序并以一种更加美观的方式输出。
'''

from urllib.request import urlopen
import json

'''
u=urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp=json.loads(u.read).decode('utf-8')
from pprint import pprint
pprint(resp)


{'completed_in': 0.074,
'max_id': 264043230692245504,
'max_id_str': '264043230692245504',
'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
'page': 1,
'query': 'python',
'refresh_url': '?since_id=264043230692245504&q=python',
'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
            'from_user': ...
            }
            {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
            'from_user': ...
            }],
'results_per_page': 5,
'since_id': 0,
'since_id_str': '0'}

'''

'''
一般来讲，JSON解码会根据提供的数据创建dicts或lists。 如果你想要创建其他类型的对象，
可以给 json.loads() 传递object_pairs_hook或object_hook参数

'''


s='{"name":"name","share":50,"price":43980}'
from collections import OrderedDict
data=json.loads(s,object_pairs_hook=OrderedDict)
print(data)

class JSONObject:
    def __init__(self,d):
        self.__dict__=d

looo=json.loads(s,object_hook=JSONObject)
print(looo.name,looo.share,looo.price)

'''
OrderedDict([('name', 'name'), ('share', 50), ('price', 43980)])
name 50 43980
'''

#这个hook的意思应该是把 解码后的对象当做参数传给hook方法。


print(json.dumps(data,indent=4))  #如果没有indent知己放在一行。有indent就是中间的空格数
'''
{
    "name": "name",
    "share": 50,
    "price": 43980
}
'''


# 对象的实例化


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

def serialize_instance(obj):
    d={'__classname__':type(obj).__name__}
    d.update(vars(obj))
    return d

classes={'Point':Point}
def unserialize_object(d):
    clsname=d.pop('__classname__',None)  # json字符串的抛出
    if clsname:
        print(clsname,type(clsname))  #Point <class 'str'>
        cls=classes[clsname]  #classes的key必须跟类名一样。
        obj=cls.__new__(cls)
        for key,value in d.items():
            setattr(obj,key,value)
        return obj
    else:
        return d


p=Point(3,4)
s=json.dumps(p,default=serialize_instance)
print(s,type(s))
a=json.loads(s,object_hook=unserialize_object)
print(a)
# 有点意犹未尽。

