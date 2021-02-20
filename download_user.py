import os
import os.path
import sys
from datetime import datetime, timedelta
from pixivpy3 import *
import common.globalvar as c

def download_user_imgs(user_id, api, root):
    download_folder=root+"/"+str(user_id)
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    cur_count=0
    
    while True:
        json_result = api.user_illusts(user_id, offset=cur_count, type='illust')
        cur_count=cur_count+len(json_result['illusts'])
        for i in range(len(json_result['illusts'])):
            item=json_result['illusts'][i]

#            date=item["create_date"].split('T')[0]
#            image_url=""
#            if len(item["meta_single_page"])!=0:
#                image_url=item["meta_single_page"]["original_image_url"]
#                api.download(image_url, path=download_folder)
#                print(date+": "+image_url)
#            else:
#                for j in range(len(item["meta_pages"])):
#                    image_url=item["meta_pages"][j]["image_urls"]["original"]
#                    api.download(image_url, path=download_folder)
#                    print(date+": "+image_url)
        break
        if json_result["next_url"]==None:
            break

if __name__ == '__main__':
    api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    api.require_appapi_hosts()
    api.set_accept_language('en-us')
    api.login(c._USERNAME, c._PASSWORD)
    download_user_imgs(3271214, api, "./download")
