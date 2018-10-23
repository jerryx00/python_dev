#!/usr/bin/env python
# coding:utf-8
import httplib
import urllib2
import json

class JsonUtil:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def http_post(self):
        url = self.url
        jsonstr = self.data
        conn = httplib.HTTPConnection(url)
        headers = {"Content-type": "application/json"}  # application/x-www-form-urlencoded
        conn.request("POST", "/core-oper/rest/bindCard", jsonstr, headers)
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

    def http_get(self):
        url = self.url
        response = urllib2.urlopen(url)  # 调用urllib2向服务器发送get请求
        return response.read()  # 获取服务器返回的页面信息

    def http_post_by_array(self):
        url = self.url
        data = self.data
        data = json.dumps(data)  # 对数据进行JSON格式化编码
        self.data = data
        ret = url.http_post_by_json(self)
        return ret


    def http_post_by_json(self):
        url = self.url
        data = self.data
        req = urllib2.Request(url, data)  # 生成页面请求的完整数据
        response = urllib2.urlopen(req)  # 发送页面请求
        return response.read()  # 获取服务器返回的页面信息

    def http_put_array(self):
        url = self.url
        data = self.data
        data = json.dumps(data)  # 对数据进行JSON格式化编码
        self.data = data
        ret  = url.http_post_by_json(self)
        return ret

    def http_put_json(self):
        url = self.url
        data = self.data
        request = urllib2.Request(url, data)
        request.add_header('Content-Type', 'your/conntenttype')
        request.get_method = lambda: 'PUT'  # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        return request.read()

    def http_delete_array(self):
        url = self.url
        data = self.data
        data = json.dumps(data)
        self.data = data
        ret = url.http_post_by_json(self)
        return ret


    def http_delete_json(self):
        url = self.url
        data = self.data
        request = urllib2.Request(url, data)
        request.add_header('Content-Type', 'your/conntenttype')
        request.get_method = lambda: 'DELETE'  # 设置HTTP的访问方式
        request = urllib2.urlopen(request)
        return request.read()

