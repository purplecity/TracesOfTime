# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/23 3:03 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_11_1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 讲的是request  这个早就用过了
# 只不过还有text.json这种操作

from  http.client import HTTPConnection
from urllib import parse

c=HTTPConnection('www.python.org',80)
c.request("HEAD",'/index.html')
resp=c.getresponse()

print("Status",resp.status)
for name,value in resp.getheaders():
    print(name,value)


# 感觉可以跳过了这里
#反正标准库是http.client  牛逼的库就是requests就用这两个
# 包括cookie的传递  上传文件  提供自行一HTTP头  auth包含账户密码的认证等 都可以用requests
