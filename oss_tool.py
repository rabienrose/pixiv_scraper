import random 
import math
import time
import numpy as np
from os import listdir
import pymongo
import oss2
import os

oss_config = {
    'endpoint': 'oss-cn-beijing-internal.aliyuncs.com',
    #'endpoint': 'oss-cn-shanghai.aliyuncs.com',
    'bucket': 'ride-v',
    'accessKeyId': 'LTAI4GJDtEd1QXeUPZrNA4Yc',
    'accessKeySecret': 'rxWAZnXNhiZ8nemuvshvKxceYmUCzP',
}

auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])

def del_folder(oss_folder):
   for obj in oss2.ObjectIterator(bucket, prefix=oss_folder):
       bucket.delete_object(obj.key)

del_folder("maps")