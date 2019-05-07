# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 5:47 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 启动或者停止线程

from  threading import Thread
# t=Thread(target=countdown,args=(10,),daemon=True)
# t.start()

'''
你无法结束一个线程，无法给它发送信号，无法调整它的调度，也无法执行其他高级操作。如果需要这些特性，你需要自己添加
'''

# 只能将线程加到当前线程并等待它终止  t.join()
# 需要手动停止。因为线程变量是共享的


