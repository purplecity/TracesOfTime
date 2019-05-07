# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/6 6:10 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_7.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 线程池

'''
这里的主要是推崇concurrent.futures中的threadpoolExecutor。最后讲了可以设置虚拟内存的问题。2000个线程大概70m真实内存。

'''

'''
12-8 多进程编程 都是使用内置的函数
这里讲了跟上一章相同的都是concurrent.futures中的，只不过thread改为了process。可能有一些其他库会更好些。就比如requests比起内置的那些函数更好些。
而且按照最后的说法，并不支持方法，闭包和其他类型的并行执行。
'''

