# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import json

URL = "http://127.0.0.1:5000/zaiyaoshuju"
data = {'rid':"1164160"}

headers = {'Content-Type': 'application/json'}
request = urllib2.Request(url=URL, headers=headers, data=json.dumps(data))
response = urllib2.urlopen(request)

print response.read()