# 程序执行时创建一个临时文件或目录，并希望使用完之后可以自动销毁掉。

from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    f.write('helloworld\n')
    f.write('test\n')
    f.seek(0)
    data=f.read()
    print(data)


'''
TemporaryFile() 的第一个参数是文件模式，通常来讲文本模式使用 w+t ，二进制模式使用 w+b 。 
这个模式同时支持读和写操作，在这里是很有用的，
因为当你关闭文件去改变模式的时候，文件实际上已经不存在了。
 TemporaryFile() 另外还支持跟内置的 open() 函数一样的参数。

'''

with TemporaryFile('w+t',encoding='utf-8',errors='ignore') as f:
    ...

from tempfile import NamedTemporaryFile

with NamedTemporaryFile('w+t') as f:
    print('filename is:',f.name)

#和 TemporaryFile() 一样，结果文件关闭时会被自动删除掉。 如果你不想这么做，
# 可以传递一个关键字参数 delete=False 即可。所以虽然with会帮你处理。不过
# 最好还是自己手动f.close()吧

with NamedTemporaryFile('w+t', delete=False) as f:
    print('filename is:', f.name)
    ...

#临时目录

from tempfile import TemporaryDirectory
with TemporaryDirectory() as dirname:
    print('dirname is:',dirname)


'''
TemporaryFile() 、NamedTemporaryFile() 和 TemporaryDirectory() 函数
 应该是处理临时文件目录的最简单的方式了，因为它们会自动处理所有的创建和清理步骤。
  在一个更低的级别，你可以使用 mkstemp() 和 mkdtemp() 来创建临时文件和目录
  这些函数并不会做进一步的管理了。 例如，函数 mkstemp() 仅仅就返回一个原始的OS文件描述符，
  你需要自己将它转换为一个真正的文件对象。 同样你还需要自己清理这些文件。
  临时文件在系统默认的位置被创建，比如 /var/tmp 或类似的地方。 为了获取真实的位置，
  可以使用 tempfile.gettempdir() 函数。
  >>> tempfile.gettempdir()
'/var/folders/7W/7WZl5sfZEF0pljrEB1UMWE+++TI/-Tmp-'
  
'''

# 所有和临时文件相关的函数都允许你通过使用关键字参数 prefix 、suffix 和 dir 来自定义
# 目录以及命名规则。


f=NamedTemporaryFile(prefix='mytemp',suffix='.txt',dir='/tmp')
print(f.name)#  '/tmp/mytemp8ee899.txt'


