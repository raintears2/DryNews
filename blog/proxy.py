# coding=gbk

import sys

proxy_array=[]          # �����б� 
db=None                 #���ݿ�ȫ�ֶ���
conn=None
#dbfile='../blog/proxy/proxier0224.db'     #���ݿ��ļ���

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
        db.text_factory = str
        reload(sys)
        sys.setdefaultencoding('gbk')
        #db.create_function("unix_timestamp", 0, my_unix_timestamp)  
        conn  = db.cursor()
        '''
        from django.db import connection
        conn = connection.cursor()
    except:
        print "--blog/proxy.py > ����sqlite���ݿ�ʧ�ܣ���ȷ���ű�����Ŀ¼����дȨ��"
        raise SystemExit


def find_proxy ():
    open_database()

    sql = "select ip,port from proxier where active = 1 "
    conn.execute(sql)
    #print sql
    rows = conn.fetchall()   
    #conn.close()
    return rows


def UnitTest ():
    rows = find_proxy()
    print rows[0]


#UnitTest()