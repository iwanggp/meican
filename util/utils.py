# coding:utf-8
"""
订餐系统的工具类
"""
from __future__ import unicode_literals

import datetime
import time
import urllib
import urllib.parse
from util.json_util import json_dump

one_week = datetime.timedelta(weeks=1)
"""订餐的基URL
"""


def mc_params(datas):
    d = {"noHttpGetCache": int(time.time() * 1000)}
    d.update(datas)
    p = "&".join(["{}={}".format(k, v) for (k, v) in d.items()])
    return p


"""基url所有的url都是由该方法进行拼装的
"""


def get_url(url):
    mc_url = "https://meican.com/{}"
    return mc_url.format(url)  # 拼装url


def login_url():  # 登陆url
    return get_url("account/directlogin")


def is_login():  # 判断是否登陆
    return get_url("login")


# def mc_time_url():  # 获取订餐时间的url
#     return get_url("preorder/basic?{}".format(mc_params({})))


# def show_me():  # 展示个人信息的url
#     return get_url("preorder/api/v2.1/accounts/show?{}".format(mc_params({})))


def calender_items_url():  # 获取日历列表
    today = datetime.datetime.today()
    begin_date = str(today.date())
    end_date = str((today + one_week).date())
    data = {
        "beginDate": begin_date,
        "endDate": end_date,
        "withOrderDetail": False,
    }
    return get_url("preorder/api/v2.1/calendarItems/list?{}".format(mc_params(data)))


def milli_to_datetime(milliseconds):
    return datetime.date(1970, 1, 1) + datetime.timedelta(milliseconds=int(milliseconds))


def milli_strftime(milliseconds, format='%Y-%m-%d'):
    return milli_to_datetime(milliseconds).strftime(format)


def concat_target_time(tab):  # 获取可订餐时间
    return "%s %s" % (milli_strftime(tab["targetTime"]), tab["openingTime"]["closeTime"])


def restaurants_url(tab):  # 获取相应的餐厅列表及开放时间
    uid = tab["userTab"]["uniqueId"]
    data = {
        "tabUniqueId": uid,
        "targetTime": concat_target_time(tab)
    }
    return get_url("preorder/api/v2.1/restaurants/list?{}".format(mc_params(data)))


# def recommendations_url(tab):  # 获得推荐列表
#     uid = tab['userTab']['uniqueId']
#     data = {
#         "tabUniqueId": uid,
#         "targetTime": concat_target_time(tab)
#     }
#     return get_url("preorder/api/v2.1/recommendations/dishes?{}".format(mc_params(data)))


def order_url(tab, dish_ids, address_uid):  # 下单
    d_str = json_dump(dish_ids)
    order_string = urllib.parse.quote(d_str)
    data = {
        "corpAddressUniqueId": address_uid,
        "order": order_string,
        "tabUniqueId": tab['userTab']['uniqueId'],
        "targetTime": concat_target_time(tab),
        "userAddressUniqueId": address_uid
    }
    return get_url("preorder/api/v2.1/orders/add?" + mc_params(data))


# def cancle_order_url(tab, order_id):  # 取消订单
#     data = {
#         "uniqueId": order_id,
#         "type": "CORP_ORDER",
#         "restoreCart": "false",
#     }
#     return get_url("preorder/api/v2.1/orders/delete?" + mc_params(data))


def restaurant_dishes_url(tab, restaurant_uid):  # 获取餐厅列表
    data = {
        "restaurantUniqueId": restaurant_uid,
        "tabUniqueId": tab["userTab"]["uniqueId"],
        "targetTime": concat_target_time(tab)
    }
    return get_url("preorder/api/v2.1/restaurants/show?" + mc_params(data))


# 判断列表是否为空
def empty_list(list):
    return list is None or len(list) == 0


def millis():
    return int(round(time.time() * 1000))
