import mysql.connector
#import pymysql
import pandas as pd 

class dbconn:
    def __init__(self, type='local'):
        if type == 'local':
            self.conn = mysql.connector.connect(
                user='dhara', password='dhara', host='localhost', database='telegram', use_pure=True,)  # raise_on_warnings=True
        elif type == 'snowy':
            self.conn = mysql.connector.connect(user='telegram', password='telegram',
                                                host='snowy.dyn.gsu.edu', port=3307, database='telegram', use_pure=True,)
        self.cursor = self.conn.cursor(buffered=True)

    def printq(self):
        for thing in self.cursor:
            print(thing)

    def drop(self, tablename, verbose=True):
        self.cursor.execute("drop table if exists {}".format(tablename))
        if verbose:
            print("dropped table {} if existed prviously".format(tablename))
    def desc(self, tablename):
        self.cursor.execute("desc {}".format(tablename))
        self.printq()

    def select(self, tablename, limit=None):
        if not limit:
            self.cursor.execute("select * from {}".format(tablename))
        else:
            self.cursor.execute("select * from {} limit {}".format(tablename, limit))
        self.printq()
    def count_rows(self, tablename):
        self.cursor.execute("select count(*) from {}".format(tablename))
        self.printq()
    def get_tables(self):
        self.cursor.execute("show tables")
        self.printq()
    def create_table(self, tablename, createquery, verbose=True):
        self.drop(tablename, verbose)
        self.cursor.execute(createquery.format(tablename))
        if verbose:
            print("created table {}".format(tablename))
            self.desc(tablename)
        self.conn.commit()
    def fill_table_with_dataframe(self, tablename, fillrowquery, df, verbose=True):
        for i, r in df.iterrows():
            self.cursor.execute(fillrowquery.format(tablename), tuple(r))
            if i % 100000 == 0 and i:
                self.conn.commit()
            if i % 1000 == 0 and verbose:
                print("rows inserted: {}".format(i))
        self.conn.commit()
        print("rows in {}".format(tablename))
        self.count_rows(tablename)

def create_text_table(dbconn, tablename, verbose=True):
    createquery = '''
    CREATE TABLE `{}` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `mid` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtype` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `uname` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtime` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `fwd` tinyint(1) DEFAULT NULL,
    `ftime` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `funame` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `rid` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtxt` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `ftxt` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mentions` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
    )DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    dbconn.create_table(tablename, createquery)


def fill_text_table(db, tablename, df):
    query = "insert into {} (mid, mtype, uname, mtime,fwd, ftime, funame, rid, mtxt, ftxt, mentions) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(
        tablename)
    for i, r in df.iterrows():
        db.cursor.execute(query, (r.mid, r.mtype, r.uname, r.mtime, int(
            r.fwd), r.ftime, r.funame, r.rid, r.mtxt, r.ftxt, r.mentions))
        if (i % 100000) == 0 and i:
            db.conn.commit()
        if (i % 1000) == 0:
            print("rows inserted: {}".format(i))
    db.conn.commit()

def create_io_table(db, tablename, verbose=True):
    createioquery = '''
    CREATE TABLE `{}` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
        `date` varchar(45),
        `byuname` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `action` varchar(10),
        `uname` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        PRIMARY KEY (`id`)
        )DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    db.create_table(tablename, createioquery, verbose)

def fill_io_table(db, tablename, df, verbose=True):
    ioquery = "insert into {} (date, byuname, action, uname) values (%s, %s, %s, %s)"
    db.fill_table_with_dataframe(tablename, ioquery, df, verbose)
    
def create_adminactivity_table(db, tablename, verbose=True):
    createioquery = '''
    CREATE TABLE `{}` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `date` varchar(45),
    `txt` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
    )DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
    db.create_table(tablename, createioquery, verbose)

def fill_adminactivity_table(db, tablename, df, verbose=True):
    adminquery = "insert into {} (date, txt) values (%s, %s)"
    db.fill_table_with_dataframe(tablename, adminquery, df, verbose)