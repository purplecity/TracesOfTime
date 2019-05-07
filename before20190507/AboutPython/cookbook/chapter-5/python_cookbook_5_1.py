# with语句给被使用的文件创建了一个上下文环境，但with控制块结束的时候，文件会自动关闭
# 不适用with则要手动关闭文件

g=open('hello.txt','rt',newline='') #把newline这个字符转换为换行符。前面照样打印

