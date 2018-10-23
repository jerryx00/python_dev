#!/usr/bin/env python
# coding:utf-8

import datetime
import json
import logging.handlers
import os
import time
import urllib
import urllib2
from ctypes import *;

import win32com.client

# COMM_LOG_FILE = 'd:/sms.log'
LOG_PATH = 'd:/'
COMM_LOG_FILE = LOG_PATH + datetime.datetime.now().strftime('%Y-%m-%d') + "_sms.log"

HA_SMS_PORT = '5'
HA_SMS_REPORT = '1'
HA_SMS_PHONE = '10085005'
SLEEP_SECOND = 30
# 1:表示锁定状态，不可以写入或更新
ACCESS_LOCK = 0


def sms_to_send_http(data):
    msg = urllib.parse.quote(data['msg'])
    phone = HA_SMS_PHONE
    if 'user' in data:
        user = data['user']
    else:
        user = ''
    if 'passwd' in data:
        passwd = data['passwd']
    else:
        passwd = ''
    if 'passwd' in data:
        msgID = data['msgID']
    else:
        msgID = ''

    stra = ['User=' + user, ',Password=' + passwd, ',MsgID=' + msgID, 'phone=' + data['phone'], 'Msg=' + msg]
    msg_http = ','.join(stra)
    msg_http
    url = "http://127.0.0.1:9618/User=" + msg_http
    html = urllib2.urlopen(url)
    ret = json.loads(html.read())
    if ret == "00":
        print "发送成功"
    elif ret == '01':
        print "密码或口令错"
    elif ret == '02':
        print "无可发送条数"
    else:
        print "其它原因拒绝"


# target_phone 要发送的短信服务器的号码
def sms_ins_access_sql(data):
    # table = "SendingSmsTable"
    # col = "(SendNumber, SmsContent, NewFlag)"
    table = 'OutBox'

    var_col = ['username', 'Mbno', 'Msg', 'ComPort', 'Report', 'V1', 'V2']
    var_comma = ','
    valInsCol = var_comma.join(var_col)

    v_spec = "\'"
    val_v = [v_spec + data['username'] + v_spec, v_spec + data['phone'] + v_spec, v_spec + data['msg'] + v_spec,
             HA_SMS_PORT, HA_SMS_REPORT, v_spec + data['mobile'] + v_spec, v_spec + data['orderno'] + v_spec]
    valInsVal = var_comma.join(val_v)

    valInsSpec = "%s,%s,%s,%d"

    sql_statement = "INSERT INTO OutBox (" + valInsCol + ") values (" + valInsVal + ")"

    # sql_statement = 'INSERT INTO OutBox (username) values' + '(' + data['username'] + ')'
    # sql_statement = "INSERT INTO OutBox (username) VALUES(111)"
    logger.info(sql_statement)
    return sql_statement


def sms_to_send_arr(arr):
    ret = []
    phone = "10086005"
    # identify_code = arr['identify_code']
    identify_code = arr['identify_code']
    llfx_phone = arr['mobile']
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
    return arr


def sms_to_send_winexec(msg):
    # WinExec("SendSms 13988888888 生日快乐！" , SW_HIDE)
    phone = HA_SMS_PHONE
    cmd = "SendSms " + phone + " " + msg
    p = os.popen(cmd)
    ret = p.read()  # 得到的是个字符串


def sms_sent():
    table = "RecvSmsTable"


# list = cur.fetchall()


# 回调
def sme_sent_notify():
    url = "http://110.51.81/llfx/Api.php/Sms/input?telephone_num[@1]&sms_txt=[@2]&date=[@3]&sms_port=[@4]"
    html = urllib2.urlopen(url)
    ret = json.loads(html.read())
    if ret == "ok":
        print "接收成功"
    else:
        print "接收失败"


def get_orders():
    print "working......%d" % SLEEP_SECOND  # url = 'http://localhost/api.php/sms/qryorder?minid=0&appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
    url = 'http://localhost/api.php/sms/qryorder?appid=5c0uF3Q78LXSrYwZEXjUA8lYi7LRxQvW&access_token=rgoVu@yddbUUccZIWZ3fICpaVpcmNS'
    html = urllib2.urlopen(url)

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

        conn = win32com.client.Dispatch('ADODB.Connection')
        DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/DATA.mdb'
        # DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=\\192.168.1.101\edisonSms/smsdb.mdb'
        conn.Open(DSN)
        lock_db
        for i in range(0, size):
            # 写入access数据库
            # print sql_statement[i]
            conn.Execute(sql_statement[i])
        # sms_to_send_http(ret[i])

        conn.Close()
        release_db


def get_messages():
    print 'a'


def upd_messages():
    print 'a'


def smsdll():
    h = CDLL('sms.dll')
    print h.Sms_AutoFlag();
    print h.Sms_NewFlag();


def lock_db():
    ACCESS_LOCK = 1


def release_db():
    ACCESS_LOCK = 0


def work():
    # 获取未处理的订单
    get_orders()
    # 获取未读短信并更新
    get_messages()
    # 更新短信状态
    upd_messages


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
