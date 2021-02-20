# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from pixivpy3 import *

if sys.version_info >= (3, 0):
    import imp
    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True


# change _USERNAME,_PASSWORD first!
_USERNAME = "283136745@qq.com"
_PASSWORD = "La_009296"


def main():
    api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
    # api.set_additional_headers({'Accept-Language':'en-US'})
    api.set_accept_language('en-us')

    #api.login(_USERNAME, _PASSWORD)
    api.auth(refresh_token="ORVE-F2EDZAeL6EJXoRZpejEI1mm47t9WmrEXHq0Qjs")
    json_result = api.illust_ranking('day', date=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'))

    print("Printing image titles and tags with English tag translations present when available")

    for illust in json_result.illusts[:3]:
        print(illust)


if __name__ == '__main__':
    main()
