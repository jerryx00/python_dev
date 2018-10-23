# coding:utf-8
import json
from random import random

import requests
from django.http import HttpResponse, request
from django.shortcuts import render


def index(request):
    return HttpResponse(u"欢迎欢迎")

def view(request):
    str = u"我在学Django，用它来建网站"
    return render(request, 'view.html',{'str': str})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))

def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def subscriber():
    counter = 0
    while True:
        counter = counter + 1
        # time.sleep(0.5)
        subscriberOrder(counter)

#模拟用户订购订单--模拟下游
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
    # print response.text
    if (response.status_code == requests.codes.ok):
        pass
        # print '%s 提交成功 %s.' % (cnt,mobile)
    else:
        pass
        # print '%s 提交失败 %s.' % (cnt,mobile)
    # result, returnContent = http_post(url, jasonstr)
    # print result, returnContent

#模拟服务端接受数据并返回--模拟上游
def notifyOrder():
    data = json.loads(request.body)
    custom_decks = data['payload']['data']

    orderid = '1378' + str(random.randint(1000000, 9999999))
    resp = ({
        "header": {
            "errcode": "0",
            "errmsg": "提交成功"
        },
        "payload": {
            "data": {
                "orderid": orderid,
            }
        }
    })
    response = requests.post(url=url, headers=headers, data=json.dumps(req))
    # print response.text
    if (response.status_code == requests.codes.ok):
        pass
        # print '%s 提交成功 %s.' % (cnt,mobile)
    else:
        pass

    pass