import os
import sys
from datetime import datetime, timedelta
from pixivpy3 import *
import pprint
import json
import common.globalvar as c
import pymongo
url="mongodb://root:La_009296@dds-wz9322f1e49b2774-pub.mongodb.rds.aliyuncs.com:3717/admin"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]

pp = pprint.PrettyPrinter(indent=1)

def main():
    api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
    api.set_accept_language('en-us')
    #api.login(c._USERNAME, c._PASSWORD)
    api.auth(refresh_token="ORVE-F2EDZAeL6EJXoRZpejEI1mm47t9WmrEXHq0Qjs")
    cur_count=0
    follow_list = mydb["following"]
    all_following=list(follow_list.find({},{"_id":0,"id":1}))
    user_dict={}
    for item in all_following:
        user_dict[item["id"]]=1
    new_user=[]
    while True:
        json_result = api.user_following(c.my_id, offset=cur_count)
        cur_count=cur_count+len(json_result["user_previews"])
        for key in json_result["user_previews"]:
            user_info={}
            user_info["id"]=key['user']['id']
            user_info["name"]=key['user']['name']
            if not user_info["id"] in user_dict:
                new_user.append(user_info)
        if json_result["next_url"]==None:
            break
    follow_list.insert_many(new_user)
    for x in follow_list.find({},{"_id":0}):
        print(x)
    

if __name__ == '__main__':
    main()
