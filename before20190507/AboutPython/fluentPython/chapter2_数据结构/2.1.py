# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/7 10:35 PM                               
#  Author           purplecity                                       
#  Name             2.1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Python 也从 ABC 那里继承了用统一的风格去处理序列数据这一特点。
# 不管是哪种数据结构，字符串、列表、字节序列、数组、XML 元素，
# 抑或是数据库查询结果，它们都共用一套丰富的操作：迭代、切片、排
# 序，还有拼接。


# 首先就是序列类型

# 序列类型是用c实现的

#容器序列 list tuple collection.deque 可以存放不同类型 不同类型 不同类型
# str bytes bytearray memoryview array.array只能存放一种类型 一种类型--字符字节数值

#容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列
#里存放的是值而不是引用。换句话说，扁平序列其实是一段连续的内存
#空间。由此可见扁平序列其实更加紧凑，但是它里面只能存放诸如字
#符、字节和数值这种基础类型。


# 类型都在builtin.py中可以找到

# bytearray 和bytes的区别 https://www.cnblogs.com/gundan/p/8047315.html builtin.py中定义就知道了

