import os
import sys
from datetime import datetime, timedelta
from pixivpy3 import *
import pprint
import json
import common.globalvar as c
import pymongo
import oss2
import ffmpeg
#url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41591-pub.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42307-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
image_list = mydb["images"]
oss_config = {
    'endpoint': 'oss-cn-beijing-internal.aliyuncs.com',
    #'endpoint': 'oss-cn-shanghai.aliyuncs.com',
    'bucket': 'pixivchamo',
    'accessKeyId': 'LTAI4GJDtEd1QXeUPZrNA4Yc',
    'accessKeySecret': 'rxWAZnXNhiZ8nemuvshvKxceYmUCzP',
}
raw_root="raw_imgs"
display_root="display_imgs"
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])
pp = pprint.PrettyPrinter(indent=1)

def resize_img(img_file):
    probe = ffmpeg.probe(img_file)
    video_stream = probe["streams"][0]
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    if width>height:
        new_height=480
        new_width=int(new_height*(width/height))
    else:
        new_width=480
        new_height=int(new_width*(height/width))
    print(new_width)
    print(new_height)
    (
        ffmpeg
        .input(img_file)
        .filter('scale', new_width, new_height)
        .output("small_"+img_file)
        .run()
    )


def main():
    max_count = image_list.count_documents({"moe":{ "$exists" : False }})
    count=0
    for x in image_list.find({"moe":{ "$exists" : False }},{"_id":0,"file_name":1}):
        count=count+1
        print(str(count)+"/"+str(max_count))
        image_file=x["file_name"]
        exist = bucket.object_exists(raw_root+"/"+image_file)
        if exist:
            bucket.get_object_to_file(raw_root+"/"+image_file, image_file)
            resize_img(image_file)
            bucket.put_object_from_file(display_root+"/"+image_file, "small_"+image_file)
            myquery = { "file_name": image_file }
            newvalues = { "$set": { "moe": 0} }
            image_list.update_one(myquery, newvalues)
            os.remove(image_file)
            os.remove("small_"+image_file)
            
if __name__ == '__main__':
    main()
