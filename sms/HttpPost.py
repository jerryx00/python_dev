#coding=utf-8
import os
import urllib
import urllib2
import re
import cookielib
import json


port = '80'
headers = {}
headers['Content-Type'] = 'application/json; charset=utf-8'
route = 'Api.php/Kmauth/notify'
url = "http://127.0.0.1:%s/%s" % (port, route)


def jsonPost(url, values):
	post_data = urllib.urlencode(values)
	j_data = json.dumps(values)
	req = urllib2.Request(url, j_data, headers)
	page = urllib2.urlopen(req)
	res = page.read()
	page.close()
	return res

values = {}
values["uuid"] = 'XXXXX'
values['uid'] = '86945'


res = jsonPost(url, values)
print res