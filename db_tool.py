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

def list_db(myclient):
    for db in myclient.list_databases():
        print(db)

pp = pprint.PrettyPrinter(indent=1)
follow_list = mydb["following"]
count=0
# follow_list.update_many({},{"$set":{"download":0,"last_create":0}})
# list_db(myclient)
# for coll in mydb.list_collection_names():
#     print(coll)
for x in follow_list.find({},{"_id":0}):
    if not "download" in x:
        print(count, x)
        break
    count=count+1
