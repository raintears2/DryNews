#coding=gbk
'''

ע�⣺���ļ���ֻ��ʵ��һ�Σ����б�������ȫ�ֹ���

'''

db=None                 #���ݿ�ȫ�ֶ���
conn=None
dbfile='data.db'     #���ݿ��ļ���
createtable=1       

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
        db = sqlite.connect(dbfile,isolation_level=None)    
        db.text_factory = str
        #print(sys.getdefaultencoding())
        reload(sys)
        sys.setdefaultencoding('gbk')
        conn  = db.cursor()
    except:
        print "����sqlite���ݿ�ʧ�ܣ���ȷ���ű�����Ŀ¼����дȨ��"
        raise SystemExit

    sql="""
       /* id:     ��ˮ�� */
       /* hname:     ¥������ */
       /* price:     ���� */
       /* area:     Ƭ�� */
       /* city:     ʡ�� */
       /* county:     ���� */
       /* addr:     ��ַ */
       /* type:     �������� */
       /* class:     ��ҵ��� */
       /* right_year:     ��Ȩ���� */
       /* right_type:     ��Ȩ���� */
       /* gross_area:     ������� */
       /* land_area:     ռ����� */
       /* direction:     ��λ */
       /* huxing_size:     ������� */
       /* plot_ratio:     �ݻ��� */
       /* Greening_rate:     �̻��� */
       /* total_homes:     �ܻ��� */
       /* developer:     ������ */
       /* PM_fee:     ��ҵ�� */
       /* metro:     �������/���� */
       /* start_date:     ����ʱ�� */
       /* comp_date:     ����ʱ�� */
       /* open_date:     ����ʱ�� */
       /* avail_time:     ��סʱ�� */
       /* parking:     ��λ�� */

        CREATE TABLE IF NOT EXISTS  `house` (
            `id` varchar(20) NOT NULL default '',    
            `hname` varchar(30) NOT NULL default '',    
            `price` varchar(30) NOT NULL default '',
            `area` varchar(30) NOT NULL default '',
            `city` varchar(30) NOT NULL default '',
            `county` varchar(30) NOT NULL default '',
            `addr` varchar(300) NOT NULL default '',
            `type` varchar(30) NOT NULL default '',
            `class` varchar(30) NOT NULL default '',
            `right_year` varchar(30) NOT NULL default '',
            `right_type` varchar(30) NOT NULL default '',
            `gross_area` varchar(30) NOT NULL default '',
            `land_area` varchar(30) NOT NULL default '',
            `direction` varchar(30) NOT NULL default '',
            `huxing_size` varchar(30) NOT NULL default '',
            `plot_ratio` varchar(30) NOT NULL default '',
            `Greening_rate` varchar(30) NOT NULL default '',
            `total_homes` varchar(30) NOT NULL default '',
            `developer` varchar(30) NOT NULL default '',
            `PM_fee` varchar(30) NOT NULL default '',
            `metro` varchar(30) NOT NULL default '',
            `start_date` varchar(30) NOT NULL default '',
            `comp_date` varchar(30) NOT NULL default '',
            `open_date` varchar(30) NOT NULL default '',
            `avail_time` varchar(30) NOT NULL default '',
            `parking` varchar(30) NOT NULL default '',

          PRIMARY KEY (`id`)                    /*  ���� */
        );
        /*
        CREATE INDEX IF NOT EXISTS `area`        ON proxier(`area`);
        CREATE INDEX IF NOT EXISTS `county`   ON proxier(`county`);
        CREATE INDEX IF NOT EXISTS `type`       ON proxier(`type`);
        CREATE INDEX IF NOT EXISTS `class`      ON proxier(`class`);
        */
        PRAGMA encoding = "utf-8";      /* ���ݿ��� utf-8���뱣�� */
    """
    if createtable:
        conn.executescript(sql)
    

    
def add_to_db(item):
    sql="""insert into `house` (
        `id`
        ,`hname`
            ,`price`
            ,`area`
            ,`city`
            ,`county`
            ,`addr`
            ,`type`
            ,`class`
            ,`right_year`
            ,`right_type`
            ,`gross_area`
            ,`land_area`
            ,`direction`
            ,`huxing_size`
            ,`plot_ratio`
            ,`Greening_rate`
            ,`total_homes`
            ,`developer`
            ,`PM_fee`
            ,`metro`
            ,`start_date`
            ,`comp_date`
            ,`open_date`
            ,`avail_time`
            ,`parking`
        ) values
    ('"""
    for i in range(len(item)):
        sql += item[i]+","

    sql += "')"
    try:
        conn.execute(sql)
    except:
        pass 
        