#coding:utf-8
"""
主函数
"""
import os,sys

from api import Meican
import datetime
import requests
import schedule
sys.setdefaultencoding('utf8')

if not sys.version_info[0]==3:#如果python版本不是3.0以上则结束程序
    print("error:only support python3.x.")
    sys.exit()
import json
import collections
import random
mc=Meican()
def main():
    with open("users.json","r") as f:
        users=json.load(f)
    random.shuffle(users)
    for user in users:
        if login(user):
            print("Success!!!!")
def login(users):
    if "username" in users and "password" in users:
        username=users['username']
        password=users['password']
        if username=="" or password=="":
            print("error: please 'username' or 'password' in users.json")
            return False
        print(">>"*20,username,"<<"*20)
        if mc.cookies_login(username) or mc.login(username,password):
            return True
        else:
            return False
    else:
        print("error:please 'username' or 'password' in users.json")
        return False
if __name__=="__main__":
    main()