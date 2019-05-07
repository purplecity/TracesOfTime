# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/5 8:35 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_1.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 终于进入这本书的正题了MMP

'''


!r 就是 repr
!s 就是 str
!a 就是 ascii

"Harold's a clever {0!s}"　　　　　# Calls str() on the argument first
"Bring out the holy {name!r}"　　# Calls repr() on the argument first
"More {!a}"　　　　　　　　　　# Calls ascii() on the argument first
'''

# '{0.x},{0.y}'.format()  0指的是类本身