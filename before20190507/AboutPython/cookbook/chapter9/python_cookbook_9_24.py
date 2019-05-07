# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 7:54 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_24.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 高级操作 AST  抽象语法数

import ast
ex=ast.parse('2+3*4+x',mode='eval')
print(ex)
print(ast.dump(ex))

#Expression(body=BinOp(left=BinOp(left=Num(n=2), op=Add(), right=BinOp(left=Num(n=3), op=Mult(), right=Num(n=4))), op=Add(), right=Name(id='x', ctx=Load())))

#算了太底层的操作跳过。  留下ast dis  源码操作吧跟最后c操作一样的暂时留下不堪。具体debug就看日志了。