import os
import sys
from datetime import datetime, timedelta
import pprint
import json
import common.globalvar as c
import pymongo
import oss2
import time
import nltk
from nltk.tokenize import RegexpTokenizer

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


def main():
    nltk.download('punkt')
    count=0
    token_stats={}
    tokenizer = RegexpTokenizer(r'\w+')
    for img_table_name in mydb.list_collection_names():
        print(img_table_name)
        img_table=mydb[img_table_name]
        for x in img_table.find({}):
            for item in x["tags"]:
                if item["translated_name"] is not None:
                    tokens = tokenizer.tokenize(item["translated_name"])
                    tokens=[tokens.lower() for tokens in tokens if tokens.isalpha()]
                    for t in tokens:
                        if t not in token_stats:
                            token_stats[t]=1
                        else:
                            token_stats[t]=token_stats[t]+1
        f=open("token_stats.json","w")
        json.dump(token_stats, f)
        
    count=0
    for key in token_stats:
        if token_stats[key]>10:
            count=count+1
    print(len(token_stats), count)
if __name__ == '__main__':
    main()
