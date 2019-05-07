# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/14 9:42 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_13_1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 13.1 fileinput
# 13.2 直接raise 异常类来退出，并给出信息
# 13.3 超越sys.argv  使用argparse模块。正式。要用的时候采纳
# 13.4 小东西。可以
# 13.5 可以最后一一句话其实有些复杂的原理还是有必要了解的。
# 13.6 可以就是python中执行shell语句 2个
#  a=subprocess.check_output("grep python|wc > out"
# shlex.quote  官方文档最好

# 13.7 复制或者移动文件目录而不用shell。 good。
# 其实就是shtil 和 os.path函数。前者还提供了忽略某些文件的方法和错误异常类
# 13.8 还是shutil 创建和解压归档文件
# 13.9  不用调用shell 也实现了一些shell不能做的功能。但还是一个脚本。比如通过文件名查找文件
# os.walk() os.path good
'''
#是遍历一个顶层目录下的所有目录。这个顶层目录还可以是相对路径格式。这个查找文件牛逼
import os

def finefile(start,name):
    for relpath,dirs,files in os.walk(start):
        print(relpath)
        if name in files:
            full_path=os.path.join(start,relpath,name)
            print(os.path.normpath(os.path.abspath(full_path)))

finefile("../../","readme.txt")
'''


#打印一个目录下所有最近被修改过的文件。time.time()函数确实是秒

'''
import os
import time

def modified_within(top,seconds):
    now=time.time()
    for path,dirs,files in os.walk(top):
        for name in files:
            fullpath=os.path.join(path,name)
            if os.path.exists(fullpath):
                mtime=os.path.getmtime(fullpath)
                if mtime>(now-seconds):
                    print(fullpath)
'''

# 13.10  读取配置文件
# configparser读取配置文件.虽然说set能设置，也能读取。但是文件实际没变化，这是亲测的


# 13.11 给简单脚本增加日志功能 之前用了
# 13.12 也是日志ok
# 13.13 这个可以。time_perf_counter()和time.process_time()可以保证最精准的时间。不过那个定义异常函数。然后函数中抛出一类异常类实例。这样好像不是重点
# 13.14 你想对在Unix系统上面运行的程序设置内存或CPU的使用限制，子进程数量，打开文件数等等。用到resource模块。这个可以暂时不看。但是可以记住了限制cpu和内存。真是good
# 13.15卧槽到最后还都是模块.不过这个功能就是代码来打开浏览器。那可以通过代码打开其他窗口吗。想想这又是挺酷