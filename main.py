# coding:utf-8
"""
主函数
"""
import os, sys

import time

from api import Meican
import datetime
import schedule

if not sys.version_info[0] == 3:  # 如果python版本不是3.0以上则结束程序
    print("error:only support python3.x.")
    sys.exit()
import json
import random

mc = Meican()
curr_day = datetime.datetime.now().weekday()#获得当前是周几
def main():
    with open("users.json", "r") as f:
        users = json.load(f)
    random.shuffle(users)
    for user in users:
        if login(user):
            mc.mc_order()
            print("Success!!!!")


def login(users):
    if "username" in users and "password" in users:
        username = users['username']
        password = users['password']
        if username == "" or password == "":
            print("error: please 'username' or 'password' in users.json")
            return False
        print(">>" * 20, username, "<<" * 20)
        if mc.cookies_login(username) or mc.login(username, password):
            return True
        else:
            return False
    else:
        print("error:please 'username' or 'password' in users.json")
        return False


if __name__ == "__main__":
    schedule.every().day.at("16:58").do(main)
    while True:
        print("xiaomei is working.............")
        if curr_day not in [5,6]:#工作日订餐，非工作日排除
            print("now i am ready to order dish for you..............")
            schedule.run_pending()
            time.sleep(10)
