import os
import sys
from datetime import datetime, timedelta
import pprint
import json
import common.globalvar as c
import pymongo
import oss2
import ffmpeg
import time

use_internal=True
acce_endpoint="oss-accelerate.aliyuncs.com"
internal_endpoint="oss-cn-shenzhen-internal.aliyuncs.com"
if use_internal:
    endpoint=internal_endpoint
    url="mongodb://root:La_009296@dds-wz9322f1e49b2774118430.mongodb.rds.aliyuncs.com:3717/admin"
else:
    endpoint=acce_endpoint
    url="mongodb://root:La_009296@dds-wz9322f1e49b2774-pub.mongodb.rds.aliyuncs.com:3717/admin"
oss_config = {
    'endpoint': endpoint,
    'bucket': 'aidraw',
    'accessKeyId': 'LTAI4FsWehTR7PpKcXVHkEkH',
    'accessKeySecret': 'dca5YKQMoXB5at6Xs4kEV9KwQVi5Tw',
}
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])
pp = pprint.PrettyPrinter(indent=1)
img_size=512
def convert_img(img_file):
    probe = ffmpeg.probe(img_file)
    video_stream = probe["streams"][0]
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    aspect_rate=width/height
    if width<256 or height<256 or aspect_rate<0.5 or aspect_rate>2:
        print("size:", width, height)
        return False
    (
        ffmpeg
        .input(img_file)
        .filter('scale', img_size, img_size,force_original_aspect_ratio=1)
        .filter('pad', img_size, img_size,width/2,height/2,color="white")
        .output("pad_"+img_file)
        .global_args('-loglevel', 'error')
        .run()
    )
    return True


def main():
    count=0
    for img_table_name in mydb.list_collection_names():
        print(img_table_name)
        img_table=mydb[img_table_name]
        for x in img_table.find({"status":{"$exists":False},"total_bookmarks":{"$gt":100}}):
            user_id=x["user_id"]
            create_date=x["create_date"]
            for item in x["imgfiles"]:
                oss_img_path="raw_imgs/"+str(user_id)+"/"+str(create_date)+"_"+item
                try:
                    bucket.get_object_to_file(oss_img_path, item)
                    re =convert_img(item)
                    if re:
                        bucket.put_object_from_file("train_imgs/"+item, "pad_"+item)
                        count=count+1
                        print(count,item)
                        img_table.update_one({"id":x["id"]},{"$set":{"status":2}})
                        os.remove("pad_"+item)
                    else:
                        img_table.update_one({"id":x["id"]},{"$set":{"status":-1}})
                    os.remove(item)
                except:
                    print('oss error!!!!')
                    time.sleep(10)
                    break
if __name__ == '__main__':
    main()
