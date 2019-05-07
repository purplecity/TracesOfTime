# 上个星期5的时间

from datetime import  datetime,timedelta

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']


def get_previous_byday(dayname,start_data=None):
    if start_data is None:
        start_data = datetime.today()
        print(start_data)
    day_num=start_data.weekday()  #weekday 0-6 对应周1-日
    print(day_num)
    day_num_target=weekdays.index(dayname) #取第一个下标
    print(day_num_target)
    days_ago=(7+day_num-day_num_target)%7
    if days_ago==0:
        days_ago=7
    target_date=start_data-timedelta(days=days_ago)
    return target_date

print(datetime(2018,7,15).weekday()) #6
print(get_previous_byday('Tuesday'))

'''
6
2018-07-16 11:11:05.700235
0
1
2018-07-10 11:11:05.700235
'''

# 有更快的方法  pip install python-dateutil

from dateutil.relativedelta import relativedelta
from dateutil.rrule import  *
d=datetime.now()
print(d)

#next friday
print(d+relativedelta(weekday=FR))
#last friday
print(d+relativedelta(weekday=FR(-1)))

'''
2018-07-16 11:16:55.553434
2018-07-20 11:16:55.553434
2018-07-13 11:16:55.553434
'''

