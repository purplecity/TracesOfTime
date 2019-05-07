#  时间单位转换，指定日期时间等
from datetime import  timedelta
a=timedelta(days=2,hours=5)
b=timedelta(hours=4.5)
print(a+b)
c=a+b
print(c.seconds,c.total_seconds()/3600)



from datetime import  datetime
x=datetime(2012,3,14)
print(x+timedelta(days=10))
y=datetime(2012,5,23)
print(b-a)
print((b-a).days)
print(datetime.today(),datetime.today()+timedelta(minutes=20))

'''
2 days, 9:30:00
34200 57.5
2012-03-24 00:00:00
-3 days, 23:30:00
-3
2018-07-16 10:47:01.434102 2018-07-16 11:07:01.434107

'''