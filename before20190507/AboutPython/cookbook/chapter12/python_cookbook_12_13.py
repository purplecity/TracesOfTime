# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/13 7:47 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_13.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# select的轮训应该就是去list中的socket。不然就是去找对应的fileno方法暴露出底层所用描述符。
# 卧槽一个队列定义了fileno方法让select可以轮询。吗的。其实就是轮询多个队列。

# 12——14

# 在unix系统上启动守护进程  linux操作了。我们只知道nohup。