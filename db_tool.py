import os
import sys
from datetime import datetime, timedelta
# from pixivpy3 import *
import pprint
import json
import common.globalvar as c
import pymongo
url="mongodb://root:La_009296@dds-wz9322f1e49b2774-pub.mongodb.rds.aliyuncs.com:3717/admin"
# url="mongodb://root:La_009296@dds-wz9322f1e49b2774118430.mongodb.rds.aliyuncs.com:3717/admin"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]

def list_db(myclient):
    for db in myclient.list_databases():
        print(db)

pp = pprint.PrettyPrinter(indent=1)
follow_list = mydb["following"]
count=0
# follow_list.update_many({},{"$set":{"download":0,"last_create":0}})
# list_db(myclient)

def serch_imgid(id):
    for coll in mydb.list_collection_names():
        if not "imginfo" in coll:
            continue
        image_table=mydb[coll]
        for x in image_table.find({"id":id}):
            print(x)
            quit()

def process_db():
    count1=0
    count2=0
    count3=0
    for coll in mydb.list_collection_names():
        if not "imginfo" in coll:
            continue
        image_table=mydb[coll]
        for x in image_table.find({"status":{"$exists":False},"total_bookmarks":{"$gt":100}}):
            # if not "imgfiles" in x:
            #     print("data error:",x["id"])
            #     continue
            # file_list=x["imgfiles"]
            page_count=x["page_count"]
            # new_file_list=[]
            # old_count=len(file_list)
            # count1=count1+1
            count3=count3+page_count
            # print(count1,count3)
            # if page_count==old_count:
            #     continue
            # for item in file_list:
            #     if not item in new_file_list:
            #         new_file_list.append(item)
            
        print(count3)
            # image_table.update_one({"id":x["id"]},{"$set":{"imgfiles":new_file_list}})
            
# for x in follow_list.find({},{"_id":0}):
#     print(count, x)
#     count=count+1
# for x in mydb["imginfo_202102"].find({"id":87689415},{"_id":0}):
#     print(count, x)
#     break
process_db()
# serch_imgid(56978079)

    
