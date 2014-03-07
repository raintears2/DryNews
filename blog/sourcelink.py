#coding=utf-8

'''
2014.2.26

1��ʹ�ô��������
2��ʹ�ö��̣߳�ÿ�߳�ʹ�ò�ͬ�Ĵ��������
3��ץȡ���д�����ݿ�
'''

from time import sleep
import os, sys, urllib2, re, threading, thread, time, datetime
import urllib2opener as prxurl2

debug = 0
# �ļ��洢·��


db=None                 #���ݿ�ȫ�ֶ���
conn=None
cur_path = os.path.dirname(__file__)
#dbfile='../blog.db.sqlite3'     #���ݿ��ļ���
mutex = threading.Lock()
daemonSubTimeOut = 60     #�����̣߳��ػ���������ʱ�ޣ��������߳��������ã���������������Ӱ�����߳�
debug = 0
#�ػ����̣߳��й涨�Ľ���ʱ�䣬�����������߳���֮����
def daemonSub (tHandles,timeout=30):
    if debug:
        print '--sourcelink.py > daemonSub() is start.',threading.active_count(),'/',datetime.datetime.now()
    
    for thi in tHandles:
        thi.daemon = True
        thi.start()

    if debug:
        print '--sourcelink.py > daemonSub() is finish.',threading.active_count(),'/',datetime.datetime.now()


def open_database():
    global db,conn,dbfile

    try:
        from pysqlite2 import dbapi2 as sqlite
    except:
        print """
        ������ʹ�� sqlite �����ݿ����������ݣ����б�������Ҫ pysqlite��֧��
        python ���� sqlite ��Ҫ�������ַ�������ģ�� pysqlite,  272kb
        http://initd.org/tracker/pysqlite/wiki/pysqlite#Downloads
        ����(Windows binaries for Python 2.x)
        """
        raise SystemExit

    try:
        '''
        db = sqlite.connect(dbfile,isolation_level=None)   
        #print dir(db)
        db.text_factory = str
        #reload(sys)
        #sys.setdefaultencoding('utf-8')
        #db.create_function("unix_timestamp", 0, my_unix_timestamp)  
        conn  = db.cursor()
        '''
        reload(sys)
        sys.setdefaultencoding('utf-8')

        from django.db import connection
        conn = connection.cursor()
    except:
        print "--sourcelink.py > ����sqlite���ݿ�ʧ�ܣ���ȷ���ű�����Ŀ¼����дȨ��"
        raise SystemExit


def getSourceLink ():
    open_database()

    sql = "select id,link,targetregex from blog_sourcelink where status = 1"
    conn.execute(sql)
    #print sql
    rows = conn.fetchall()   
    #conn.close()
    if debug:    print '--sourcelink.py > proc srclink.rows:',len(rows)
    return rows


#url������
def dispatcher():
    srclinks = getSourceLink()
    for link in srclinks:
        #print link[0],link[1]
        if debug==1: print "thrcount:",threading.active_count()
        try:
            threads = []
            i = 0
            while threading.active_count() >= 30 and i < 5:
                sleep(2) 
                if debug: print '    sleep 2 sec(a),',threading.active_count()
                i += 1
            else:
                t = threading.Thread(target = target, args = (link[0],link[1],link[2]))
                #t.start()
                #sleep(1)
                #t.join(30)
                threads.append((t))

            daemonThread = threading.Thread(target = daemonSub, args = (threads,1))
            daemonThread.start()
            daemonThread.join(daemonSubTimeOut)    
            if debug: print '--sourcelink.py > daemonThread.alive:',daemonThread.is_alive(),'/',daemonThread.ident,threading.active_count(),datetime.datetime.now()
            tcount = 0
            fcount = 0
            for th in threads:
                if th.isAlive() == True:
                    tcount += 1
                else:
                    fcount += 1
                
            if debug: print '--sourcelink.py > alive:',tcount,'+',fcount,'=',len(threads)
            if debug: print '--sourcelink.py > �������߳����'
        
        except Exception, e:
            print e


def target (id,url,pattern):
    #print url,pattern
    content = prxurl2.url_proxy_open( url )
    if debug==1: print pattern
    #if debug: print len(content)
    #print type(content)
    matchs = []
    if type(content) != type(None):
        matchs = re.findall(pattern, content)
    
    mutex.acquire()
    open_database()
    if debug==1: print len(matchs)
    newCount = 0 
    for match in matchs:
        #print item
        hashid = hash(match[1])
        #print hashid
        #print int(hashid) 
        check = "select 1 from blog_urlresult where hashid = " + str(hashid) 
        conn.execute(check)
        rows = conn.fetchall()
        if len(rows) <= 0 :
            #if debug: print match[1]
            sql = "insert into blog_urlresult (srclinkid_id,link,title,createtime,hashid) values("+str(id)+",'"+match[0]+"','"+match[1]+"',datetime('now'),"+str(hashid)+")"
            sql = unicode(sql,"gbk")
            if debug: print sql
            conn.execute(sql)
            if debug: print 'db inserted'
            newCount += 1

    if newCount > 0: 
        print '--sourcelink.py > found news: ',newCount,url
    else:
        print '--sourcelink.py > no news,done.',url
            
    #conn.close()
    mutex.release()
    thread.exit()
        

def test ():
    print '----sourcelink.test()--'
    
            
if __name__ =="__main__":
    dispatcher()    
    if debug==1: print "thrcount:",threading.active_count()
