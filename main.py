#coding:utf-8
from datetime import datetime
import urllib2
import urllib
import json
import re
import time
from datetime import datetime, timedelta
from array import *
from HTMLParser import HTMLParser
import base64
import hashlib

import MySQLdb

#主程序
def main():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    #数据库的打开
    db = MySQLdb.connect(db='mysql',host='127.0.0.1',user='root',passwd='enter0087!')
    db.autocommit(1)
    cur = db.cursor()
    cur.execute('show databases;')

    for data in cur.fetchall():
        print data

    #使用数据库
    cur.execute('use mhzrb;')

#    curr_time = time.strftime('%Y-%m/%d')
#    last_url = 'http://ehzrb.hz66.com/'+'hzrb'+'/html/'+curr_time+'/node_2.htm'
    now = datetime.now()
    i = 0
    days = 360
    while(i < days):
        delta = timedelta(days=i)
        n_days = now - delta
        i +=1
        url_time = n_days.strftime('%Y-%m/%d')
        web_time = n_days.strftime('%Y-%m-%d 00:00:00.000')

        curr_url = 'http://ehzrb.hz66.com/hzrb/html/'+url_time+'/node_2.htm'
        bHzlv = isHzlv_url(curr_url)
        if  bHzlv!=0:
            #print curr_url,bHzlv

            strSQL = 'insert ignore INTO hzlv (url,type,time,sid) VALUES(\'' + curr_url + '\',' + \
                     str(bHzlv) + ',\'' + str(web_time) + '\',\'' + \
                     base64.b64encode(hashlib.sha1(curr_url+str(bHzlv)).hexdigest()) +'\')'

            cur.execute(strSQL)
            print strSQL

#hashlib.sha1(data).hexdigest();

 #   print isHzlv_url('http://ehzrb.hz66.com/hzrb/html/2015-10/27/node_2.htm')

    #关闭数据库
    cur.close()
    db.commit()
    db.close()

    pass

#判断是否是需要的内容
def isHzlv_url(url):
    #0表示返回时没有找到旅游
    #1表示旅游
    #2表示度假区
    #3表示二个都有
    flag = 0
    #得到当前的列表
    html = urllib.urlopen(url)
    output = html.read()
    output = output.decode('gbk').encode('utf-8')

    #改内容(初次)
    restr = re.findall('<!--Right-->([\s\S]*)<!--Right End-->',output)

    if restr:
        data = re.findall('title=\'(.*?)\'>[A-Z]\d\d',restr[0])

    hzlv_filter = ('湖州旅游','度假区时报')

    if restr:
        i = 0
        for x in hzlv_filter:
            restr1 = re.findall('<a href=\'node_(\d+).htm\' title=\'[A-Z]\d\d版：'+ str(x), restr[0])
            i += 1
            if restr1:
                flag = flag + i

    return flag

#得到在数据库中最新的url
def getDBListUrl(type):
    pass


#RUN
main()
