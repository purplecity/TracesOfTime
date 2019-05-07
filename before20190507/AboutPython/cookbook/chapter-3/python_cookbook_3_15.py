# 字符串转化为日期时间。有strftime。但是性能差

#如果知道确切的时间格式。最好自己切割，性能快很多
# 比如 yyyy-mm-dd

from datetime import datetime
def parse_ymd(s):
    year_s,mon_s,day_s=s.split('-')
    return datetime(int(year_s),int(mon_s),int(day_s))