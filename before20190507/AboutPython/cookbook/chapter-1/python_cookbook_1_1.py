test1=(4,5)
test2=[3,4,5,'hehe',{9:4}]
test3='ikl'  # 任何可迭代对象都可以这样操作
test4=['heheehheheheh',6,7,(4,4,5)]

a,b=test1
c,d,e,f,g=test2
h,i,j=test3
_,k,l,_=test4 #多一个少一个参数都不行。而且相同_变量做占位符，如果print打印出来的时候值是最后一个.
print(a,b,c,d,e,f,g,h,i,j,k,l,_)
