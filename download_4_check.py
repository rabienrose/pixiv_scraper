import requests
import os
import os.path
import random
import math
import re
import json
import operator
import pymongo
import oss2

url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41591-pub.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42307-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
#url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
image_list =mydb["images"]
follow_list =mydb["following"]
oss_config = {
    #'endpoint': 'oss-cn-beijing-internal.aliyuncs.com',
    'endpoint': 'oss-cn-beijing.aliyuncs.com',
    'bucket': 'pixivchamo',
    'accessKeyId': 'LTAI4GJDtEd1QXeUPZrNA4Yc',
    'accessKeySecret': 'rxWAZnXNhiZ8nemuvshvKxceYmUCzP',
}
raw_root="raw_imgs"
local_cache_root="raw_imgs"
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])
if __name__ == '__main__':
    type = 0
    info={}
    count=0
    start_download=False
    for user in follow_list.find({}):
        user_id=user["id"]
        if user_id==3388329:
            start_download=True
        if start_download==False:
            continue
        count=count+1
        max_count=image_list.count_documents({"user_id":user_id})
        print(str(user_id)+"/"+str(max_count))
        os.mkdir(local_cache_root+"/"+str(user_id))
        for x in image_list.find({"user_id":user_id}):
        #for x in image_list.aggregate([{"$match":{"moe":0}},{"$sample": {"size":1000}}]):
            
            image_file=x["file_name"]
            bucket.get_object_to_file(raw_root+"/"+image_file, local_cache_root+"/"+str(user_id)+"/"+image_file)
            #image_list.update_one({"file_name":image_file},{"$set":{"moe":-1}})
