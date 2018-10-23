import urllib2
import json
import urllib
import win32com.client
import os
import time


def work():
    print "let's work."
    while True:
	  url = 'http://192.168.1.102/llfxdev/api.php/sms/qryorder?minid=0&appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
	  html = urllib2.urlopen(url)

	  hjson = json.loads(html.read())

	  errcode = hjson['errcode']
	  size = hjson['size']
	  reqid = hjson['reqid']
	  data = hjson['data']
	  for i in range(0, size):
		  # data_order = hjson['summary']
		  print i, "get datas ok"

def runTask(func, day=0, hour=0, min=0, second=0):

  while True:
	time.sleep(10)
	work()
  db.close

runTask(work, day=1, hour=2, min=1)