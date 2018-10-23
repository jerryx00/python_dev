#!/usr/bin/env python
# coding:utf-8
import datetime
import sys

import win32com.client

import Util
import types

reload(sys)
sys.setdefaultencoding('utf-8')


class AccessModel:
    # COMM_LOG_FILE = 'd:/sms.log'
    LOG_PATH = 'D:\sms_order\logs'
    COMM_LOG_FILE = LOG_PATH + datetime.datetime.now().strftime('%Y-%m-%d') + "_sms.log"
    HA_SMS_PORT = '5'
    HA_SMS_REPORT = '1'
    HA_SMS_PHONE = '10085005'
    SLEEP_SECOND = 60
    # 1:表示锁定状态，不可以写入或更新
    ACCESS_LOCK = 0

    def __init__(self, dataUrl):
        self.dataUrl = dataUrl
        ###定义conn

    def db_conn(self):
        conn = win32com.client.Dispatch(r'ADODB.Connection')
        dns = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=' + self.dataUrl
        conn.Open(dns)
        return conn
        ####定义rs

    def db_rs(self):
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.CursorType = 1
        rs.CursorLocation = 3
        rs.LockType = 3
        return rs
        ####关闭数据库

    def db_close(self):
        conn = self.db_conn()
        conn.Close()
        ####获取数据库所有记录集

    def db_query_table(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        print sql
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        dataStr = ""
        arrData = []
        if rs.RecordCount == 0:
            rs.Close()
            self.db_close()
            return arrData

        rs.MoveFirst()
        while (rs.EOF == False and rs.BOF == False):
            i = 0
            dataStr = "{"
            while i < rs.Fields.Count:
                strField = rs.Fields(i).name
                strField = str(strField).lower()
                strMsg = str(rs.Fields(i).value).strip()
                # strMsg = strMsg.strip('\n')
                # strMsg = strMsg.strip('\r')
                if (strField == 'msgtitle'):
                    strTemp = strMsg.split();
                    strMsg = "".join(strTemp);
                strMsg = unicode(strMsg, "utf8")
                strMsg = strMsg.encode("utf-8")

                dataStr += "\"" + strField + "\"" + ":" + "\"" + strMsg + "\""
                if (i < rs.Fields.Count - 1):
                    dataStr += ","
                i = i + 1
            dataStr += "}"
            arrData.append(dataStr)  # JSON数据
            rs.MoveNext()
        rs.Close()
        self.db_close()
        # print arrData
        return arrData

    def db_query_inbox(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        print sql
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        dataStr = ""
        arrData = []
        if rs.RecordCount == 0:
            return arrData

        rs.MoveFirst()
        while (rs.EOF == False and rs.BOF == False):
            i = 0
            dataStr = "{"
            while i < rs.Fields.Count:
                strField = rs.Fields(i).name
                strField = str(strField).lower()
                msg = str(rs.Fields(i).value).strip()
                if (strField == 'msg'):
                    util = Util.Util(msg)
                    strMsg = util.getMobile()
                else:
                    strMsg = msg

                dataStr += "\"" + strField + "\"" + ":" + "\"" + strMsg + "\""
                if (i < rs.Fields.Count - 1):
                    dataStr += ","
                i = i + 1
            dataStr += "}"
            arrData.append(dataStr)  # JSON数据
            rs.MoveNext()
        rs.Close()
        self.db_close()
        print arrData
        return arrData

    def db_query_inbox(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        print sql
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        dataStr = ""
        arrData = []
        if rs.RecordCount == 0:
            return arrData

        rs.MoveFirst()
        while (rs.EOF == False and rs.BOF == False):
            i = 0
            dataStr = "{"
            while i < rs.Fields.Count:
                strField = rs.Fields(i).name
                strField = str(strField).lower()
                msg = str(rs.Fields(i).value).strip()
                if (strField == 'msg'):
                    util = Util.Util(msg)
                    strMsg = util.getMobile()
                else:
                    strMsg = msg

                dataStr += "\"" + strField + "\"" + ":" + "\"" + strMsg + "\""
                if (i < rs.Fields.Count - 1):
                    dataStr += ","
                i = i + 1
            dataStr += "}"
            arrData.append(dataStr)  # JSON数据
            rs.MoveNext()
        rs.Close()
        self.db_close()
        # print arrData
        return arrData

    # 该方法只返回msg,返回结果有限
    def db_query_msg(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        print sql
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        dataStr = ""
        arrData = []
        if rs.RecordCount == 0:
            return arrData

        rs.MoveFirst()
        while (rs.EOF == False and rs.BOF == False):
            i = 0
            while i < rs.Fields.Count:
                strField = rs.Fields(i).name
                strField = str(strField).lower()
                msg = str(rs.Fields(i).value).strip()
                util = Util.Util(msg)
                strMsg = util.getMobile()
                # 当msg字段值为空时,不处理了
                if (strMsg != '' and strField == 'msg'):
                    dataStr = "{"
                    dataStr += "\"" + strField + "\"" + ":" + "\"" + strMsg + "\""
                    dataStr += ","
                    dataStr += "}"
                    arrData.append(dataStr)  # JSON数据
                i = i + 1

            rs.MoveNext()
        rs.Close()
        self.db_close()
        # print arrData
        return arrData

    # 返回信息比较全
    def db_query_msg_ret(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        print sql
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        arrData = []
        if rs.RecordCount == 0:
            return arrData

        rs.MoveFirst()
        while (rs.EOF == False and rs.BOF == False):
            i = 0
            ids= ""
            row_cnt = rs.Fields.Count
            while i < row_cnt:
                strField = rs.Fields(i).name
                strField = str(strField).lower()
                strMsg = str(rs.Fields(i).value).strip()

                if (strField == 'id'):
                    ids += '"' + strField + '"' + ":" + '"' + strMsg + '"'
                    ids += ","

                if (strField == 'arrivetime'):
                    ids += '"' + strField + '"' + ":" + '"' + strMsg + '"'
                    ids += ","

                # 当msg字段值为空时,不处理了
                util = Util.Util(strMsg)
                strMsg = util.getMobile()
                if (strMsg != '' and strField == 'msg'):
                    strRetField1 = "result"
                    # 成功0, 失败1
                    strRetVal1 = util.getResult()

                    strRetField2 = "fluxnum"
                    strRetVal2 = util.getFluxnum()
                    dataStr = "{"
                    dataStr += ids
                    ids = ""
                    if (strField == 'msg'):
                        strField='mobile'
                    dataStr += '"' + strField + '"' + ":" + '"' + strMsg + '"'
                    dataStr += ","

                    dataStr += '"' + strRetField1 + '"' + ":" + '"' + strRetVal1 + '"'
                    dataStr += ","

                    dataStr += '"' + strRetField2 + '"' + ":" + '"' + strRetVal2 + '"'
                    if (i < row_cnt - 1):
                        dataStr += ","
                    dataStr += "}"
                    arrData.append(dataStr)
                i = i + 1

            rs.MoveNext()
        rs.Close()
        self.db_close()
        # print arrData
        return arrData



        ####增加记录

    def db_add(self, sql):
        # sql="insert into addresslist(name,department,cellphone) values('name','department','13xxxxxxxxxx')";
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False
            ####修改记录

    def db_modi(self, sql):
        # sql="update addresslist set name='name' where id=2"
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False
            ####删除记录

    def db_modi_inbox(self, ids):
        sql="update Msg_InBox set Readed=1 where id in (" + ids + ")"
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False
            ####删除记录

    def db_modi_table(self, ids, table):
        sql="update " + table + " set upload=1 where id in (" + ids + ")"
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False
            ####删除记录

    def db_modi_inbox_all(self, ids):
        sql = "update Msg_InBox set upload=1 where id in (" + ids + ")"
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False
            ####删除记录


    def db_del(self, sql):
        # sql="delete * from addresslist where id=2"
        try:
            conn = self.db_conn()
            conn.execute(sql)
            conn.Close()
            return True
        except (TypeError, ValueError) as e:
            conn.Close()
            return False

            ####获取数据库记录总数

    def db_recordcount(self, sql):
        conn = self.db_conn()
        rs = self.db_rs()
        rs.Open(sql, conn)
        # print (rs.RecordCount)
        count = 0
        if (rs.EOF == False and rs.BOF == False):
            count = rs.RecordCount

        rs.Close()
        self.db_close()
        return count
