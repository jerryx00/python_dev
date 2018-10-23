#!/usr/bin/env python
# coding:utf-8

import datetime
import json
import logging.handlers
import time
import urllib2
import urllib

import win32com.client

import AccessModel
import os
import JsonUtil
import Message

# COMM_LOG_FILE = 'd:/sms.log'
LOG_PATH = 'd:/sms_order/logs/'
DB_PATH = "C:/Program Files/酷卡/"
dataUrl = DB_PATH + "MMSCRM.mdb"
dataLockUrl = DB_PATH + "MMSCRM.ldb"
dataUrl = unicode(dataUrl, "utf8")


COMM_LOG_FILE = LOG_PATH + datetime.datetime.now().strftime('%Y-%m-%d') + "_sms.log"
COMM_LOG_FILE_ORDER = LOG_PATH + datetime.datetime.now().strftime('%Y-%m-%d') + "_orders.log"

HA_SMS_PORT = '31'
HA_SMS_REPORT = '1'
HA_SMS_PHONE = '10086005'
SLEEP_SECOND = 30
# 1:表示锁定状态，不可以写入或更新
ACCESS_LOCK = 0

CARD_MBNO = '106581391256052945'

SVR_URL = 'http:/xx:8080/llfx/'
#SVR_URL = 'http://localhost:80/'

#短信
HA_SMS_MSGTYPE="0"

sql = "Select ID,MsgArrivedTime as arrivetime,CommPort,MsgType,Sender,MsgTitle as msg FROM MSG_Inbox WHERE MsgType=0 AND Readed<>1 AND Sender='10086'"
# sql = "Select id,arrivetime,mbno,readed,msg FROM InBox"

# target_phone 要发送的短信服务器的号码
def sms_ins_access_sql(data):
    # table = "SendingSmsTable"
    # col = "(SendNumber, SmsContent, NewFlag)"
    table = 'MSG_Outbox'

    # var_col = ['Sender', 'Receiver', 'MsgType', 'MsgTitle', 'CommPort']
    var_col = ['Receiver', 'MsgType', 'MsgTitle', 'CommPort']
    var_comma = ','
    valInsCol = var_comma.join(var_col)
    # print valInsCol
    v_spec = "\'"
    # val_v = [v_spec + data['username'] + v_spec, v_spec + data['phone'] + v_spec, v_spec + data['msg'] + v_spec,
    #          HA_SMS_PORT, HA_SMS_REPORT, v_spec + data['mobile'] + v_spec, v_spec + data['orderno'] + v_spec]
    # val_v = [v_spec + HA_SMS_PHONE + v_spec, HA_SMS_MSGTYPE , v_spec + data['msg'] + v_spec,  HA_SMS_PORT ]
    val_v = [v_spec + HA_SMS_PHONE + v_spec, HA_SMS_MSGTYPE, v_spec + data['msg'] + v_spec, data['port']]

    valInsVal = var_comma.join(val_v)
    # print valInsVal
    sql_statement = "INSERT INTO MSG_Outbox (" + valInsCol + ") values (" + valInsVal + ")"
    # print sql_statement
    # sql_statement = 'INSERT INTO OutBox (username) values' + '(' + data['username'] + ')'
    # sql_statement = "INSERT INTO OutBox (username) VALUES(111)"
    logger.error(sql_statement)
    return sql_statement


def sms_to_send_arr(arr):
    ret = []
    phone = "10086005"
    # identify_code = arr['identify_code']
    identify_code = arr['identify_code']
    llfx_phone = arr['mobile']
    commport = arr['commport']
    # d1d2 = arr['d1d2']  # 生效时间 D1当有生效，D2次月生效
    d1d2 = "D1"
    # KT#535047344461226628#D1#18852308887
    var_list = ['KT', identify_code, d1d2, llfx_phone]
    var_c = '#'
    # msg = "KT#".join(identify_code).join("#").join(d1d2).join("#").join(llfx_phone)
    msg = var_c.join(var_list)
    ret = [phone, msg]

    retsms = []
    arr['phone'] = phone
    arr['msg'] = msg
    arr['port'] = commport
    return arr


# 获取订单并写入发件箱
def get_orders():
    print "working......%d" % SLEEP_SECOND  # url = 'http://localhost/api.php/sms/qryorder?minid=0&appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
    url = SVR_URL + 'api.php/sms/qryorder?appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
    try:
        html = urllib2.urlopen(url, timeout=10)
        hjson = json.loads(html.read())

        errcode = hjson['errcode']
        errmsg = hjson['errmsg']
        size = hjson['size']
        reqid = hjson['reqid']
        data = hjson['data']
        ret = [1] * size
        sql_statement = [1] * size
        print "待处理的订单条数为 : %d" % size
        logger.info("待处理的订单条数为 : %d" % size)


        if size != 0:
            for i in range(0, size):
                # data_order = hjson['summary']
                print " 处理第: %d条记录" % (i + 1)
                ret[i] = sms_to_send_arr(data[i])
                sql_statement[i] = sms_ins_access_sql(ret[i])

            data = AccessModel.AccessModel(dataUrl)
            conn = data.db_conn()

            for i in range(0, size):
                # 写入access数据库
                print sql_statement[i]
                conn.Execute(sql_statement[i])
            # sms_to_send_http(ret[i])

            conn.Close()
    except:  # 将异常对象输出
        print("error:get_orders, api.php/sms/qryorder" )


# 处理收件箱短信
def get_messages():
    try:
        data = AccessModel.AccessModel(dataUrl)
        # log = Util.Util(COMM_LOG_FILE_ORDER)

        # sql = "Select * FROM InBox WHERE Readed <>0 AND mbno='" + CARD_MBNO + "'"

        dataRecordSet = data.db_query_msg_ret(sql)
        mapdict = dict()
        i = 0

        for item in dataRecordSet:
            a = eval("(" + item + ")")  # eval解析JSON数据
            # print (a['msg'])  # Msg为字段名
            i = i + 1
        mapdict['size'] = i
        mapdict['dataList'] = dataRecordSet

        url = SVR_URL + 'api.php/Kmauth/notify?appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'

        strRet = jsonPost2(url, mapdict)
        logger.info("Server Kmauth/notify ret:%s" % strRet)
        # 输入两位 ok认为正常，否则接口返回失败信息
        # print strRet
        json_to_python = json.loads(strRet)
        result = json_to_python['result']

        if (result != '0') :
            logger.info("服务器返回结果为1,数据格式错误")
            print "服务器返回结果为1,数据格式错误"
        else:
            strOk = json_to_python['ok']
            strFail = json_to_python['fail']
            if (strOk != ''):
                ids = json_to_python['ok']
                # print ids
                dataRecordSet = data.db_modi_inbox(ids)


    except :  # 将异常对象输出
        print("error:get_messages" )


# 处理收件箱短信(全部发给服务器)
def get_msg_inbox_all(table, action):
    try:
        data = AccessModel.AccessModel(dataUrl)
        # log = Util.Util(COMM_LOG_FILE_ORDER)

        sql_msg_inbox = "Select * FROM " + table + " WHERE upload <> 1"
        # sql_msg_inbox = "Select * FROM " + table + " "

        dataRecordSet = data.db_query_table(sql_msg_inbox)
        mapdict = dict()
        i = 0

        for item in dataRecordSet:
            strItem = unicode(item, "utf8")
            # eval解析JSON数据
            a = eval("(" + strItem + ")")
            # print (a['msgtitle'])  # Msg为字段名
            i = i + 1

        # if (i == 0):
            # return
        mapdict['size'] = i
        mapdict['dataList'] = dataRecordSet

        url = SVR_URL + 'api.php/sms/' + action + '?appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
        # print url
        strRet = jsonPost2(url, mapdict)
        logger.info("Server sms/" + action + " ret:%s" % strRet)
        # 输入两位 ok认为正常，否则接口返回失败信息
        # print strRet
        json_to_python = json.loads(strRet)
        result = json_to_python['result']

        if (result != '0') :
            logger.info(action + "服务器返回结果为1,数据格式错误")
            print action + "服务器返回结果为1,数据格式错误"
        else:
            strResult = json_to_python['result']

            if (strResult == '0'):
                ids = json_to_python['ids']
                # print ids
                if (ids != ''):
                    dataRecordSet = data.db_modi_table(ids, table)


    except :  # 将异常对象输出
        print("error:get_msg_inbox_all" )


def jsonPost(url, values):
    jdata = json.dumps(values)  # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
    response = urllib2.urlopen(req)  # 发送页面请求
    return response.read()  # 获取服务器返回的页面信息

def jsonPost(url, values, headers):
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    values = urllib.urlencode(values)
    values = json.dumps(values)
    req = urllib2.Request(url, values, headers)
    page = urllib2.urlopen(req)
    res = page.read()
    page.close()
    return res

def jsonPost2(url, values):
    headers = {}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    # values = urllib.urlencode(values)
    values = json.dumps(values)
    req = urllib2.Request(url, values, headers)
    page = urllib2.urlopen(req)
    res = page.read()
    page.close()
    return res

def work():

    # 获取未处理的订单,并写入发件箱
    get_orders()
    time.sleep(60)

    # 获取未读短信,并通知服务器,根据 服务器返回，更新本地收件箱信息为已读
    get_messages()
    time.sleep(1)
    # 通知服务器更新
    # 如果报备器返回成功，则更新本地短信状态为已读状态

    #将其它数据全部报给服务器
    time.sleep(1)
    get_msg_inbox_all('Msg_inbox', 'msginbox')
    time.sleep(1)
    get_msg_inbox_all('Msg_sentbox', 'msgsentbox')


def runTask(func, day=0, hour=0, min=0, second=0):
    while True:
        print "开始时间 : %s" % time.ctime()
        work()
        time.sleep(SLEEP_SECOND)
        print "结束时间 : %s" % time.ctime()
        # smsdll();




# 以下是用来处理日志的
handler = logging.handlers.RotatingFileHandler(COMM_LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

runTask(work, day=1, hour=2, min=1)
