# coding:utf-8
import pickle
import random
from functools import reduce

import urllib.parse
import requests
import requests.utils
from util.objutil import dict_obj, dict_item_obj
from util.utils import *
import json, os


class OrderTimeItem(object):
    def __init__(self, hour, min):
        super(OrderTimeItem, self).__init__()
        self.hour = hour
        self.min = min


class OrderDesc(object):
    def __init__(self):
        super(OrderDesc, self).__init__()
        self.desc = ""

    def append_dish(self, dish_item, dish_count):
        self.desc = "%s name:[%s],count:[%s] |" % (
            self.desc, dish_item.name, dish_count)

    def get_desc(self):
        return self.desc


# 构造访问头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0",  # 用户只能为pc
    "Host": "www.meican.com"  # 主域名
}


class Meican():
    def __init__(self):
        self._clear()
        self.login_ok = False
        self.close_time_list = []

    def _clear(self):
        self.session = requests.Session()
        self.session.headers = headers

    def post(self, url, data=None):
        response = self.session.post(url, data=data)
        if response.status_code == 200:
            self.session.headers['Referer'] = response.url
        return response

    def get(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            self.session.headers['Referer'] = response.url
        return response

    def save_cookie(self,username):
        with open(username+'.cookies', 'wb') as f:
            cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
            pickle.dump(cookies_dic, f)

    def load_cookie(self,username):
        with open(username+'.cookies', 'rb') as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    # 检查是否处于登陆状态
    def check_login(self):
        response = self.get(is_login())
        if response.status_code == 200 and len(response.history) > 0:
            return True
        else:
            return False

    # 初次登陆
    def login(self, username, password):
        self._clear()
        url = login_url()
        post_data = {
            "username": username,
            "password": password,
            "loginType": "username",
            "remember": "true",
            "redirectUrl": ""
        }
        response = self.post(url, post_data)
        if response.status_code == 200 and len(response.history) > 0:  # 登陆成功
            self.save_cookie(username)  # 保存cookie
            print(username + "login sucess!")
            return True
        else:
            print("login fail.")
            return False

    # 使用cookies登陆
    def cookies_login(self, username):
        self._clear()
        cook_file = "meican_cookie.cookies"
        if not os.path.exists(cook_file):
            print("cookies login fail: " + username + ".cookes not exists.")
            return False
        self.load_cookie(username)
        if not self.check_login():
            print("cookies login fail:" + username + ".cookies expire")
            return False
        print("cookies login success")
        return True

    # def account_show_info(self):  # 显示个人信息
    #     print(show_me())
    #     user_info = json.loads(self.get(show_me()).content)
    #     user_info = dict_obj(user_info)
    #     return user_info

    # def get_close_time_lst(self):
    #     return self.close_time_list

    # 获取订餐时间
    # def get_order_time_lst(self):
    #     order_time = []
    #     close_lst = self.close_time_list
    #     for time_str in close_lst:
    #         t_item = time_str.split(":")
    #         hour, minute = DateUtil.date_diff_min(int(t_item[0]), int(t_item[1]),
    #                                               int(ConfigUtil.instance().ahead_min) * -1)
    #         order_time.append(OrderTimeItem(hour, minute))
    #         pass
    #     return order_time

    # def mc_time(self):  # 获取服务器时间
    #     mc_time_info = json.loads(self.get(mc_time_url()).content)
    #     return mc_time_info

    def calendar_items(self):  # 获取日历列表，美餐的一般为一周的订餐
        return json.loads(self.get(calender_items_url()).content)

    def get_restaurants(self, tab):  # 获取餐厅类别
        return json.loads(self.get(restaurants_url(tab)).content)['restaurantList']

    # def get_recommends(self, tab):  # 获取推荐订餐列表
    #     return json.loads(self.get(recommendations_url(tab)).content)

    def get_dish_list(self, tab, restaurant_uid):  # 获得食品列表
        return json.loads(self.get(restaurant_dishes_url(tab, restaurant_uid)).content)['dishList']

    def order_request(self, tab, dish_ids, address_uid):  # 请求订单
        return json.loads(self.post(order_url(tab, dish_ids, address_uid)).content)

    def restaurant_dish_list(self, tab):  # 获得食品列表
        restaurant = self.get_restaurants(tab)
        if empty_list(restaurant):
            return None
        non_fruit = [_restaurant for _restaurant in restaurant if _restaurant['name'] != '甜仕']  # 去除甜仕的餐厅
        fruit = [_restaurant for _restaurant in restaurant if _restaurant['name'] == '甜仕']  # 获得甜仕的餐厅
        restaurant_index = random.randint(0, len(non_fruit) - 1)  # 随机的选择一个餐厅，初步解决吃什么的难题
        restaurant_uid = non_fruit[restaurant_index]['uniqueId']  # 获得餐厅的唯一编号
        dish_lst = self.get_dish_list(tab, restaurant_uid)
        dish_lst = [item for item in dish_lst if item['isSection'] is False]#去除总类产品的id如套餐或者粉之类的总称，这类编号订餐是不成功的
        print(dish_lst)
        dish_lst = dict_item_obj(dish_lst)
        return dish_lst

    # def tab_close_time(self):  # 获取关门时间
    #     close_time_lst = []
    #     data_list = self.calendar_items()['dateList']
    #     for c_item in data_list[0]['calendarItemList']:
    #         close_time = c_item['openingTime']['closeTime']
    #         close_time_lst.append(close_time)
    #     return close_time_lst

    def available_tabs(self):
        data_list = self.calendar_items()['dateList']
        avaliable = data_list[0]['calendarItemList'][0]
        address_id = avaliable['userTab']['corp']['addressList'][0]['uniqueId']  # 获得餐厅的地址编号默认是15楼
        return avaliable, address_id

    def gen_order_dish(self, dish_item, dis_count, order_desc):
        order_desc.append_dish(dish_item, dis_count)
        return {"count": dis_count, "dishId": int(dish_item.id)}

    def mc_order(self):  # 最后的一步订餐了
        tab, address_id = self.available_tabs()
        dish_ids = self.restaurant_dish_list(tab)
        main_lst = []
        side_lst = []
        dis_count = 1
        select_dish = []
        order_desc = OrderDesc()
        for dish_item in dish_ids:
            main_lst.append(dish_item)
        main_index = random.randint(0, len(main_lst) - 1)  # 随机的选择一种食品，彻底的解决了今天吃什么的难题
        side_lst.insert(0, main_lst[main_index])
        for dish_item in side_lst:
            select_dish.append(self.gen_order_dish(dish_item, dis_count, order_desc))
        print(select_dish)
        self.order_request(tab,select_dish,address_id)


if __name__ == "__main__":
    mc = Meican()
    mc.login("wanggongpeng@fc.com", "Fc12345678")
    mc.mc_order()
