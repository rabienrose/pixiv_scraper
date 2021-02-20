# -*- coding: utf-8 -*-
import json

_USERNAME = "283136745@qq.com"
_PASSWORD = "009296"
my_id=5933166


def load_following():
    f = open("user_list.json", "r")
    re_data = json.load(f)
    f.close()
    return re_data
