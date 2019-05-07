import re
comment=re.compile(r'/\*(.*?)\*/')
text1='/* this is a comment*/'
text2='''/* this is a 
multiline comment*/
'''

print(comment.findall(text1))
print(comment.findall(text2))

#[' this is a comment']
#[]

comment=re.compile(r'/\*((?:.|\n)*?)\*/')  # *?确保最短匹配 ?:确保不保留分隔符 .|\n确保或者
print(comment.findall(text2))