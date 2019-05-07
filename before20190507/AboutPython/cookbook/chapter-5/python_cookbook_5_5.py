# 文件不存在才能写入
#因为wb wt模式都会清空重写
# 使用xb xt就好了




with open('/Users/purplecity/a.txt','xt') as f:
    f.write('hello\n')
    #FileExistsError: [Errno 17] File exists: '/Users/purplecity/a.txt'

    