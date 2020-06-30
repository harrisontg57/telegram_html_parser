from dbutils import *
#db = dbconn('snowy')

drop_query = 'drop table if exists {}'
createquery = '''
    CREATE TABLE `{}` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `mid` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cid` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtype` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `uname` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtime` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `mtxt` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `img_loc` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `links` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `cname` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
    )DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    '''
showquery = 'show tables'
selectquery = 'select * from {}'

insertquery = "insert into {}(mid, cid, mtype, uname, mtime, mtxt, img_loc, links, cname) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

def create_channel_table(db, tname):
    db.cursor.execute(drop_query.format(tname))
    db.cursor.execute(createquery.format(tname))
    #db.cursor.execute(showquery)
    db.cursor.execute(selectquery.format(tname))
    db.printq()
