# coding:utf-8
"""
python 日期工具类
"""
import math
import time, datetime
from dateutil.relativedelta import relativedelta


class DateUtil(object):
    def __init__(self):
        super(DateUtil, self).__init__()

    @staticmethod
    def to_date(time):
        return datetime.datetime.fromtimestamp(time)

    @staticmethod
    def totimestap(dt, epoch=datetime.datetime(1970, 1, 1, 0, 0, 0)):
        return (dt + datetime.timedelta(seconds=time.timezone) - epoch).total_seconds()

    @staticmethod
    def add_timstamp(ts, *args):
        d = DateUtil.to_date(ts)
        b = d + relativedelta(args)
        return DateUtil.totimestap(b)

    @staticmethod
    def get_timestamp():
        return time.time()

    @staticmethod
    def get_mon_timestamp(mon):
        ts = DateUtil.get_timestamp()
        ar = {"months": mon}
        return DateUtil.add_timstamp(ts, ar, mon)

    @staticmethod
    def date_diff_min(hour, min, r_min):
        d1 = datetime.datetime.now()
        d2 = datetime.datetime(d1.year, d1.month, d1.day, hour, min)
        d3 = d2 + relativedelta(minutes=r_min)
        return d3.hour, d3.minute

    # 日常日期转换成python日期
    @staticmethod
    def convert_wday(week):
        return week - 1

    # python日期转换为日常星期
    @staticmethod
    def convert_week(day):
        return day + 1
    @staticmethod
    def curr_week():
        wday=datetime.datetime.now().weekday()
        return DateUtil.convert_week(wday)
