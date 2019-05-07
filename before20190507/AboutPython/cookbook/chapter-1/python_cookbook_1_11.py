# slicea indices

items = [0, 1, 2, 3, 4, 5, 6]

s='letgoletgo'
a=slice(5,50,2)
print(type(a))  # <class 'slice'>
print( type( a.indices( len(s) ) ) )  #<class 'tuple'>
print(a.indices(len(s)))
for i in range(*a.indices(len(s))):
    print(s[i])

'''
<class 'slice'>
<class 'tuple'>
(5, 10, 2)
l
t
o

'''


#The reverse situation occurs when the arguments are already in a list or tuple but need to be unpacked for
#  a function call requiring separate positional arguments. For instance, the built-in range() function expects
#  separate start and stop arguments. If they are not available separately, write the function call with the *-operator
# to unpack the arguments out of a list or tuple:
#In the same fashion, dictionaries can deliver keyword arguments with the **-operator:


# slice range indices都是接受三个参数 start,stop,step.
# slice类型为slice indices是slice调用indices方法，重新设置stop值

# pack和unpack
def func_tuple(*args):  # packing
    print(type(args))
    for i in args:
        print(i)


def func_dict(**dict):  # packing
    print(type(dict))
    for i in dict:
        print(i)

def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

if __name__ == '__main__':
    t = (1, 2, 3, 'hello')
    d = {'a': 1, 'b': 2, 'c': 3}
    func_tuple(*t)  # unpacking
    func_dict(**d)

    d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
    parrot(**d)


'''
<class 'tuple'>
1
2
3
hello
<class 'dict'>
a
b
c
-- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !
'''