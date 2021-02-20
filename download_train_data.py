import os
import sys
from datetime import datetime, timedelta
import pprint
import json
import common.globalvar as c
import pymongo
import oss2
import time
acce_endpoint="oss-accelerate.aliyuncs.com"
oss_config = {
    'endpoint': acce_endpoint,
    'bucket': 'aidraw',
    'accessKeyId': 'LTAI4FsWehTR7PpKcXVHkEkH',
    'accessKeySecret': 'dca5YKQMoXB5at6Xs4kEV9KwQVi5Tw',
}
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])
local_temp="./img_cache"

def main():
    count=0
    if not os.path.exists(local_temp):
        os.makedirs(local_temp)
    for obj in oss2.ObjectIterator(bucket, prefix="train_imgs"):
        try:
            file_name=obj.key.split("/")[-1]
            if len(file_name)>0:
                bucket.get_object_to_file(obj.key, local_temp+"/"+file_name)
                count=count+1
                print(count,file_name)
        except:
            print('oss error!!!!')
            time.sleep(10)
            break

if __name__ == '__main__':
    main()
