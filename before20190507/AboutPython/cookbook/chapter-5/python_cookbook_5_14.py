# 忽略文件名编码

# 你想使用原始文件名执行文件的I/O操作，也就是说文件名并没有经过系统默认编码去解码或编码过。

#所有的文件名都会根据 sys.getfilesystemencoding() 返回的文本编码来编码或解码

import sys
print(sys.getfilesystemencoding())



