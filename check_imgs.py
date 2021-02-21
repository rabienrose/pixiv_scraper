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

def main():
    dirs = os.listdir("./data/img_cache")
    for item in dirs:
        probe = ffmpeg.probe("./data/img_cache/"+item)
        video_stream = probe["streams"][0]
        width = int(video_stream['width'])
        if width!=512:
            print(item)
if __name__ == '__main__':
    main()
