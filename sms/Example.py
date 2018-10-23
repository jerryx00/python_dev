#!/usr/bin/env python
# coding:utf-8
import os
import urllib

import AccessModel
import JsonUtil
import httplib
import json
import httplib
import urllib2


CARD_MBNO = '106581391256052945'
dataUrl =  "C:\\DATA_1.mdb"






def jsonPost(url, values):
    jdata = json.dumps(values)  # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
    response = urllib2.urlopen(req)  # 发送页面请求
    return response.read()  # 获取服务器返回的页面信息


####示例
def Forexample():
    try:
        data = AccessModel.AccessModel(dataUrl)


        # sql = "Select * FROM InBox WHERE Readed <>0 AND mbno='" + CARD_MBNO + "'"
        sql = "Select id,arrivetime,mbno,readed,msg FROM InBox"
        dataRecordSet = data.db_query_msg(sql)
        a = []
        i = 0
        for item in dataRecordSet:
            a = eval("(" + item + ")")  # eval解析JSON数据
            # print (a['Msg'])  # Msg为字段名
        JsonStr = json.dumps(dataRecordSet, ensure_ascii=False, encoding='UTF-8')
        url = 'http://localhost/api.php/Kmauth/notify'
        strRet = jsonPost(url, JsonStr)
        #输入两位 ok认为正常，否则接口返回失败信息
        # ret = str[0:2]
        json_to_python = json.loads(strRet)
        result = json_to_python['result']
        print result
        if (result == '0'):
            ids = json_to_python['ids']
            print ids
            dataRecordSet = data.db_modi_inbox(ids)


    except (TypeError, ValueError) as e:  # 将异常对象输出
        print("error:" + str(e))


def query_db():
    try:
        data = AccessModel.AccessModel(dataUrl)

        # sql = "Select * FROM InBox WHERE Readed <>0 AND mbno='" + CARD_MBNO + "'"
        sql = "Select * FROM InBox WHERE Readed=0"
        dataRecordSet = data.db_query(sql)
        a = []
        i = 0
        for item in dataRecordSet:
            a = eval("(" + item + ")")  # eval解析JSON数据
            print (a['Msg'])  # Msg为字段名
        JsonStr = json.dumps(dataRecordSet, ensure_ascii=False, encoding='UTF-8')
        jsonPost()

    except (TypeError, ValueError) as e:  # 将异常对象输出
        print("error:" + str(e))


def upd_db():
    data = AccessModel.AccessModel(dataUrl)
    sql = "update OutBox set V3='0001' where id<192"
    if (data.db_modi(sql)):
        print("修改完成！")
    else:
        print("修改失败")

def del_db():
    sql = "delete * from OutBox where id<184"
    data = AccessModel.AccessModel(dataUrl)
    if (data.db_modi(sql)):
        print("删除成功！")
    else:
        print("删除失败")

Forexample()