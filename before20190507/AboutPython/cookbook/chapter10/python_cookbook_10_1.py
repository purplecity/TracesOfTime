

'''
10.2   当使用’from module import *’ 语句时，希望对从模块或包导出的符号进行精确控制

# 在你的模块中定义一个变量 __all__ 来明确地列出需要导出的内容。

其实就是from module import * 会导入__all__中所有的

10.3
mypackage/
    __init__.py
    A/
        __init__.py
        spam.py
        grok.pu

    B/
        __init__.py
        bar.py

mypackage/A/spam.py
from . import grok
from ..B import bar
from mypackage.A import grok

含有相对路径的作为脚本执行的时候要python -m

10.4

程序分成多个文件

# mymodule.py
class A:
    def spam(self): print('A.spam')

class B(A):
    def bar(self): print("B.bar")

mymodule/
    __init__.py
    a.py
    b.py

a.py
class A:
    def spam(self): print(“A.spam”)

b.py
from .a import A
class B(A):
    def bar(self): print(“B.bar”)

__init__.py
from .a import A
from .b import B

import mymodule
a=mymodule.A()   #因为是import mymodule  然后init中from .a import A.所以需要这样
a.spam()

or
from mymodule import A,B
a=A()
b=B()


延迟加载

__init__.py
def A():
    from .a import A
    return A()

def B():
    from .b import B
    return B()

import mymodule
a=mymodule.A()
a.spam()

if isinstance(x,mymodule.A) error
if isinstance(x,mymodule.a.A) ok


10-5

你可能有大量的代码，由不同的人来分散地维护。每个部分被组织为文件目录，如一个包。然而，你希望能用共同的包前缀将所有组件连接起来，不是将每一个部分作为独立的包来安装。

从本质上讲，你要定义一个顶级Python包，作为一个大集合分开维护子包的命名空间。这个问题经常出现在大的应用框架中，框架开发者希望鼓励用户发布插件或附加包。


值得一读。 假设spam是个大型软件。 下面的不同代码分散到不同人在不同的目录下。而且这样合并也很方便

10-6

reload已经改动的先前加载的模块
import spam
import imp
imp.realod(spam)

一般命令行比较多吧


reload()擦除了模块底层字典的内容，并通过重新执行模块的源代码来刷新它。模块对象本身的身份保持不变。因此，该操作在程序中所有已经被导入了的地方更新了模块。


#避免重新加载模块。
10-7运行目录或者压缩文件

这个666  就是__main__.py文件 。然后直接运行目录或者zip文件就会执行__main__.py文件
# 10.8  读取位于包中的数据文件

mypackage/
    __init__.py
    somdata.dat
    spam.py

# spam.py
import pkgutil
data=pkgutil.get_date(__package__,"domdata.dat")
由此产生的变量是包含该文件的原始内容的字节字符串



后面值得一读

10-9:


myapplication.pth
/some/dir
/other/dir

10-10

import importlib
math=importlib.import_module("math")
math.sin(2)
mod=importlib.import_module("urllib.request")
u=mod.urlopen("http://www.python.org")

mport_module只是简单地执行和import相同的步骤，但是返回生成的模块对象。你只需要将其存储在一个变量，然后像正常的模块一样使用。

如果你正在使用的包，import_module()也可用于相对导入。但是，你需要给它一个额外的参数。例如：

b=importlib.import_module(".b",__package__)

10-11
设计导入语句的扩展功能，即自定义import

10-14.. over
10-15  妈的最后来一句 设计到C扩展的代码打包分发就更复杂点了...

10-11 10-12暂时没看了。这个具体需要看吧。现在要快点结束cookbook 准备bitmex了
































'''

