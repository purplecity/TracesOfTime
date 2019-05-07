# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 6:19 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_21.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def typed_property(name, expected_type):
    storage_name = '_' + name

    @property
    def prop(self):
        print(self)
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        print(self)
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))
        setattr(self, storage_name, value)

    return prop

# Example use
class Person:
    name = typed_property('name', str)
    # print(name,type(name)) <property object at 0x1034a6958> <class 'property'>
    age = typed_property('age', int)

    '''
    def __init__(self, name, age):
        self.name = name
        self.age = age
    '''
    def __init__(self, name, age):
        self.x = name
        self.y = age

a=Person('ack',20)
'''
<__main__.Person object at 0x10e524550>
<__main__.Person object at 0x10e524550>
'''

#还是不习惯这个重复的命名