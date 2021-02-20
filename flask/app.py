import requests
import _thread
import os
import os.path
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import random
import math
import re
import json
import operator
import pymongo

app = Flask(__name__)
#url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41591-pub.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42307-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
url="mongodb://root:Lance1809@dds-2ze6c59cc1a69bf41.mongodb.rds.aliyuncs.com:3717,dds-2ze6c59cc1a69bf42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-32634159"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
image_list =mydb["images"]

@app.route('/set_moe', methods=['GET', 'POST'])
def set_moe():
    img_name = request.args.get('img_name')
    val = int(request.args.get('val'))
    image_list.update_one({"file_name":img_name},{"$set":{"moe":val}})
    return {"re":1}
    
@app.route('/set_check', methods=['GET', 'POST'])
def set_check():
    img_name = request.args.get('img_name')
    val = int(request.args.get('val'))
    image_list.update_one({"file_name":img_name},{"$set":{"check":val}})
    return {"re":1}

@app.route('/get_count', methods=['GET', 'POST'])
def get_count():
    info={}
    moe_count = image_list.count_documents({"moe":1})
    dislike_count = image_list.count_documents({"moe":-1})
    unrate_count = image_list.count_documents({"moe":0})
    check_filter={"$or":[{"check":0},{"check":{"$exists":False}}]}
    moe_uncheck_count = image_list.count_documents({"$and":[{"moe":1},check_filter]})
    dislike_uncheck_count = image_list.count_documents({"$and":[{"moe":-1},check_filter]})
    info["moe"]=moe_count
    info["dislike"]=dislike_count
    info["unrate"]=unrate_count
    info["moe_uncheck"]=moe_uncheck_count
    info["dislike_uncheck"]=dislike_uncheck_count
    return info

@app.route('/show_unrate', methods=['GET', 'POST'])
def show_unrate():
    type = int(request.args.get('type'))
    info={}
    filter={"$and":[{"moe":type}, {"$or":[{"check":0},{"check":{"$exists":False}}]}]}
    if type==0:
        filter={"moe":0}
    for x in image_list.aggregate([{"$match":filter},{"$sample": {"size":1}}]):
        info["img_file"]=x["file_name"]
        if "score" in x:
            info["score"]=x["score"]
        else:
            info["score"]="NA"
        info["type"]=x["moe"]
        break
    return info
    
@app.route('/clear_check_status', methods=['GET', 'POST'])
def clear_check_status():
    type = int(request.args.get('type'))
    image_list.update_many({"$and":[{"moe":type},{"check":1}]},{"$set":{"check":0}})

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'xxx'
    app.run('0.0.0.0', port=8001, debug=False)
