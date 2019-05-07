# any()任意  all 全部  join()连接字符入串

# 字符串开头或者结尾匹配

str.startswith()
str.endswith()
# 两个函数的参数必须是字符串。

import os
filenames=os.listdir('.')
# [ 'Makefile', 'foo.c', 'bar.py', 'spam.c', 'spam.h' ]
print([ name for name in filenames if name.endswith(('.c','.h'))])
# ['foo.c', 'spam.c', 'spam.h'
any(name.endswith('.py') for name in filenames )
# True





