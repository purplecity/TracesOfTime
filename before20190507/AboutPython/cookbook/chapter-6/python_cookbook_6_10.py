# 编码解码Base64数据
# 使用Base64格式解码或编码二进制数据

s=b'hello'
import base64

a=base64.b64encode(s)
print(a,a.decode('ascii'))
b=base64.b64decode(a)
print(b)
'''
b'aGVsbG8=' aGVsbG8=
b'hello'

'''

