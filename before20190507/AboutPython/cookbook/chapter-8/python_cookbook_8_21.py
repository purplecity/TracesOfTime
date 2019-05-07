# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/15 11:14 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_21.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 你要处理由大量不同类型的对象组成的复杂数据结构，每一个对象都需要需要进行不同的处理。 比如，遍历一个树形结构，然后根据每个节点的相应状态执行不同的操作。

# 你的意思是大量不同类型的对象组成  树这样的结构当做例子？

#已经看完。抛弃。这一节。
# 就是利用getattr来获取相应的方法。然后递归遍历。可以用生成器或者迭代器来实现非递归算法


class NodeVisitor:
    def visit(self,node):
        methname='visit' + type(node).__name__
        meth=getattr(self,methname,None)
        if meth is None:
            meth=self.generic_visit
        return meth

    def generic_visit(self,node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))


class Evaluator(NodeVisitor):
    def visit_Number(self,node):
        return node.value

    def visit_Add(self,node):
        return self.visit(node.left) + self.visit(node.right)



class HTTPHandler:
    def handle(self,request):
        methname='do_' + request.request_method
        getattr(self,methname)(request)

    def do_GET(self,request):
        pass

    def do_POST(self,request):
        pass

    def do_HEAD(self,request):
        pass