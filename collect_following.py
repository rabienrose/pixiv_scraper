import os
import sys
from datetime import datetime, timedelta
from pixivpy3 import *
import pprint
import common.globalvar as c
import time
import pymongo
import oss2

use_internal=False
acce_endpoint="oss-accelerate.aliyuncs.com"
internal_endpoint="oss-cn-shenzhen-internal.aliyuncs.com"
if use_internal:
    endpoint=internal_endpoint
else:
    endpoint=acce_endpoint
oss_config = {
    'endpoint': endpoint,
    'bucket': 'aidraw',
    'accessKeyId': 'LTAI4FsWehTR7PpKcXVHkEkH',
    'accessKeySecret': 'dca5YKQMoXB5at6Xs4kEV9KwQVi5Tw',
}
url="mongodb://root:La_009296@dds-wz9322f1e49b2774-pub.mongodb.rds.aliyuncs.com:3717/admin"
myclient = pymongo.MongoClient(url)
mydb = myclient["pixiv"]
root="./download"
oss_root="raw_imgs"
auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket'])

def cal_int_data(data_str):
    vec_str = data_str.split("T")
    day_str=vec_str[0]
    day_vec=day_str.split("-")
    day_int=int(day_vec[0]+day_vec[1]+day_vec[2])
    return day_int

def handle_img_url(item, image_url, download_folder, user_id,create_data):
    # start_time=time.time()'
    try:
        img_name = image_url.split("/")[-1]
        oss_img_name=str(create_data)+"_"+img_name
        oss_addr=oss_root+"/"+str(user_id)+"/"+oss_img_name
        if bucket.object_exists(oss_addr):
            return True
        imgfiles.append(img_name)
        api.download(image_url, path=download_folder)
        temp_file=download_folder+"/"+img_name
        bucket.put_object_from_file(oss_addr, temp_file)
        os.remove(temp_file)
    except:
        print('oss error!!!!')
        return False
    return True
    # print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    api = AppPixivAPI()  # Same as AppPixivAPI, but bypass the GFW
    # api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
    api.set_accept_language('en-us')
    #api.login(c._USERNAME, c._PASSWORD)
    api.auth(refresh_token="ORVE-F2EDZAeL6EJXoRZpejEI1mm47t9WmrEXHq0Qjs")
    follow_list = mydb["following"]
    user_count=0
    download_ver=1
    imginfo_tables={}
    for x in follow_list.find({},{"_id":0}):
        user_count=user_count+1
        print(x["id"])
        if "download" in x and x["download"]>=download_ver:
            print(x["id"],"pass download")
            continue
        cur_count=0
        if "last_create" in x:
            last_create_data=x["last_create"]
        else:
            last_create_data=0
        first_item=None
        imginfo_cache={}
        while True:
            json_result = api.user_illusts(x["id"], offset=cur_count, type='illust')
            # print(json_result['illusts'])
            if not 'illusts' in json_result:
                print('illusts is none')
                time.sleep(10)
                api = AppPixivAPI()
                api.set_accept_language('en-us')
                api.auth(refresh_token="ORVE-F2EDZAeL6EJXoRZpejEI1mm47t9WmrEXHq0Qjs")
                time.sleep(10)
                continue
            cur_count=cur_count+len(json_result['illusts'])
            end_user=False
            if json_result["next_url"] is None:
                end_user=True
            for i in range(len(json_result['illusts'])):
                item=json_result['illusts'][i]
                create_data=cal_int_data(item["create_date"])
                if last_create_data>=create_data:
                    print("exit:",last_create_data)
                    end_user=True
                    break
                if first_item is None:
                    first_item=item
                image_url=""
                vec_str = item["create_date"].split("T")
                day_str=vec_str[0]
                day_vec=day_str.split("-")
                month_str=day_vec[0]+day_vec[1]
                imginfo={}
                imginfo["create_date"]=int(day_vec[0]+day_vec[1]+day_vec[2])
                imginfo["id"]=item["id"]
                imginfo["page_count"]=item["page_count"]
                imginfo["sanity_level"]=item["sanity_level"]
                imginfo["total_view"]=item["total_view"]
                imginfo["total_bookmarks"]=item["total_bookmarks"]
                imginfo["total_comments"]=item["total_comments"]
                imginfo["tags"]=item["tags"]
                imginfo["user_id"]=item["user"]["id"]
                imginfo["title"]=item["title"]
                imgfiles=[]
                if not month_str in imginfo_cache:
                    imginfo_cache[month_str]=[]
                imginfo_cache[month_str].append(imginfo)
                if len(item["meta_single_page"])!=0:
                    image_url=item["meta_single_page"]["original_image_url"]
                    imgfiles.append(image_url.split("/")[-1])
                    while not handle_img_url(item, image_url, root, x["id"], create_data):
                        time.sleep(10)
                else:
                    for j in range(len(item["meta_pages"])):
                        image_url=item["meta_pages"][j]["image_urls"]["original"]
                        imgfiles.append(image_url.split("/")[-1])
                        while not handle_img_url(item, image_url, root, x["id"], create_data):
                            time.sleep(10)
                imginfo["imgfiles"]=imgfiles
            print("cur_count:",cur_count)
            if end_user:
                if first_item is not None:
                    create_data=cal_int_data(first_item["create_date"])
                    for key in imginfo_cache:
                        imginfo_table=None
                        if key in imginfo_tables:
                            imginfo_table=imginfo_tables[key]
                        else:
                            imginfo_table=mydb["imginfo_"+key]
                            imginfo_tables[key]=imginfo_table
                        imginfos=imginfo_cache[key]
                        for item in imginfos:
                            imginfo_table.update_one({"id":item["id"]},{"$set":item},True)
                    follow_list.update_one({"id":x["id"]}, {"$set":{"download":download_ver,"last_create":create_data}})
                    print("last_create:",create_data)
                else:
                    follow_list.update_one({"id":x["id"]}, {"$set":{"download":download_ver}})
                break
