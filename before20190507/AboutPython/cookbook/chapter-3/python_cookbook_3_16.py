# 时区问题  pip install pytz
# 日读到最后说pytz不建议使用了

'''
from pytz import  timezone
from datetime import datetime

d=datetime(2012,12,21,9,30,0)

central=timezone('US/Central')
loc_d=central.localize(d)
#转化为utc时间
utc_d=loc_d.astimezone(pytz.utc)
'''