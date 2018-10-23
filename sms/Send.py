#!/usr/bin/env python
import win32com.client

conn = win32com.client.Dispatch('ADODB.Connection')
DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=C:/smsdb.mdb'
# DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=\\192.168.1.101\edisonSms/smsdb.mdb'

conn.Open(DSN)


sql_statement = "INSERT INTO waittosendsmstable (SmsTime, PhoneNumber,SmsOperator,SmsContent, STATUS,SmsDeport,FastSms,NewFlag) VALUES('2017-03-24 21:10:03','13776620160','llfx','test msg','0','1','0',0)"
# sql_statement = "INSERT INTO waittosendsmstable (SmsTime, PhoneNumber,SmsOperator,SmsContent,STATUS,SmsDeport) VALUES('2017-03-24 21:10:03','13776620160','llfx','test msg','0','')"
sql_statement = "INSERT INTO waittosendsmstable (SmsContent) VALUES(111)"

conn.Execute(sql_statement)
conn.Close()
