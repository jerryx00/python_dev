import random
import time
import MySQLdb
import httplib
import json

# db = MySQLdb.connect("localhost", "root", "pass", "llfx")
# db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='U_njwk_0515', charset='utf8')

db.select_db('llfx');


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


def work():
    print "let's work."

    cursor = db.cursor()
    cursor.execute("select * from qw_order_init")
    data = cursor.fetchone()
    while data != None:
        print data[0], data[1], data[2]
        data = cursor.fetchone()

    url = 'localhost'
    req = ({"bindHyCardInfo": {"mobileNo": "1881026xxxx", "userId": "2", "cardno": "7926279367963021",
                               "cardpasswd": "xxxxxxxxxxxxxxx", "ip": "127.0.0.1"},
            "header": {"version": "1.0.1", "from": "1000", "to": "2000", "tid": "7926279367963021", "time": "12312",
                       "token": "SEW342WEER2342", "ext": ""}})
    jasonstr = json.JSONEncoder().encode(req)
    result, returnContent = http_post(url, jasonstr)
    print result, returnContent


def runTask(func, day=0, hour=0, min=0, second=0):
    while True:
        time.sleep(1)
        work()
    db.close





# runTask(work, min=0.5)
runTask(work, day=1, hour=2, min=1)
