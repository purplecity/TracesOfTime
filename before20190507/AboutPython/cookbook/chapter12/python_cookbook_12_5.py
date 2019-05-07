# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/30 3:06 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_5.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 你正在写一个多线程程序，其中线程需要一次获取多个锁，此时如何避免死锁问题。

# 在多线程程序中，死锁问题很大一部分是由于线程同时获取多个锁造成的。举个例子：一个线程获取了第一个锁，然后在获取第二个锁的 时候发生阻塞，那么这个线程就可能阻塞其他线程的执行，从而导致整个程序假死。 解决死锁问题的一种方案是为程序中的每一个锁分配一个唯一的id，然后只允许按照升序规则来使用多个锁，这个规则使用上下文管理器 是非常容易实现的



import threading
_local=threading.local()