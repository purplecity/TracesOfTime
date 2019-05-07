# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/1 3:04 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_7_10.py
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#带额外状态信息的回调函数

def apply_async(func,args,*,callback):
    result=func(*args)
    callback(result)


def mark_handler():
    sequence=0
    def hanle(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return hanle
def add(x,y): return x+y

hand=mark_handler()
apply_async(add,(2,3),callback=hand)