# coding:utf-8
import random
import time
import httplib
import json


# db = MySQLdb.connect("localhost", "root", "pass", "llfx")
# db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='U_njwk_0515', charset='utf8')

# db.select_db('llfx');
import requests

def http_post(url='localhost', jasonstr=''):
    conn = httplib.HTTPConnection("localhost")
    headers = {"Content-type": "application/json"}  # application/x-www-form-urlencoded
    conn.request("POST", "/core-oper/rest/bindCard", jasonstr, headers)
    response = conn.getresponse()
    data = response.read()
    if response.status == 200:
        result = "success"
        returnContent = data
    else:
        result = "fail"
        returnContent = ''
    conn.close()

    return result, returnContent


def runTask(day=0, hour=0, min=0, second=0):
    counter = 0
    while True:
        counter = counter + 1
        # time.sleep(0.5)
        subscriberOrder(counter)
        notifyOrder()



def subscriberOrder(cnt):
    url = 'http://127.0.0.1/api/llauth/order'
    headers = {'Content-Type': 'application/json'}

    # mobile = '1377' + str(random.randint(1000000, 9999999))
    mobile = 13700000000 + cnt
    req = ({
        "header": {
            "timestamp": "20161016204528",
            "type": "json",
            "identity": "201610162045281069587",
            "sign": "483cc53a1ea7628da9d436a6c0f5b1e5"
        },
        "payload": {
            "data": {
                "user": "jamsenanjing",
                "mobile": mobile,
                "operator": 1,
                "scope": 1,
                "fluxnum": 10,
                "activeflag": 0,
                "expiration": 1,
                "fluxid": "2000002",
                "orderno": "201610162045281069587",
                "backurl": "http://127.0.0.1/api/llauth/notify",
                "timestamp": "20161016204531",
            }
        }
    })
    # jasonstr = json.JSONEncoder().encode(req)

    response = requests.post(url=url, headers=headers, data=json.dumps(req))
    print response.text
    if (response.status_code == requests.codes.ok):
        print '%s 提交成功 %s.' % (cnt,mobile)
    else:
        print '%s 提交失败 %s.' % (cnt,mobile)
    # result, returnContent = http_post(url, jasonstr)
    # print result, returnContent

def notifyOrder():
   pass

# runTask(work, min=0.5)
runTask(day=1, hour=2, min=1)
