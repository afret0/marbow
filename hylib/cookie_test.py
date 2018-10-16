#-*- coding: utf-8 -*-

import sys
import cookie

if __name__ == '__main__':
    url = sys.argv[1]
    cookies = cookie.get_chrome_cookies(url)

    for key in cookies:
        print "%25s: %s" %(key, cookies[key])
