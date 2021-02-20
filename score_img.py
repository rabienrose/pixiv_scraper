import torch
import torch.nn as nn
import mobilenetv3
from PIL import Image, ImageDraw
import torchvision.transforms as transforms
import random 
import math
import time
import numpy as np
from os import listdir
import pymongo
import oss2
import os
#url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41591-pub.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42307-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"

myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
image_list = mydb["images"]
oss_config = {
    'endpoint': 'oss-cn-beijing-internal.aliyuncs.com',
    #'endpoint': 'oss-cn-beijing.aliyuncs.com',
    'bucket': 'pixivchamo',
    'accessKeyId': 'LTAI4GJDtEd1QXeUPZrNA4Yc',
    'accessKeySecret': 'rxWAZnXNhiZ8nemuvshvKxceYmUCzP',
}
raw_root="raw_imgs"
train_root="train_imgs"
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])
pre_model="./chamo.pth"

device = torch.device("cpu")
net = mobilenetv3.MobileNetV3_Small()
net.load_state_dict(torch.load(pre_model))
net.eval()
net.to(device)
input_list=[]
trans_toTensor = transforms.ToTensor()
max_count=image_list.count_documents({})
count=0
for x in image_list.find({},{"_id":0,"file_name":1}):
    count=count+1
    print(str(count)+"/"+str(max_count))
    image_file=x["file_name"]
    exist = bucket.object_exists(train_root+"/"+image_file)
    input_list = []
    if exist:
        bucket.get_object_to_file(train_root+"/"+image_file, image_file)
        img=Image.open(image_file).convert('RGB')
        input = trans_toTensor(img)
        input = input * 2 - 1
        input_list.append(input)
        input_batch = torch.stack(input_list)
        input_batch = input_batch.to(device)
        out = net(input_batch)
        score = out.tolist()
        myquery = { "file_name": image_file }
        newvalues = { "$set": { "score": round(score[0][1],2)} }
#        img.save("re/score_"+str(score[0][1])+".jpg")
        image_list.update_one(myquery, newvalues)
        os.remove(image_file)

