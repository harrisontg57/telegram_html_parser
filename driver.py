#%%
from html_parser_full_channel import *
from dbdriver import *

try:
    #checks for message htmls
    files = (subprocess.check_output(['ls', sys.argv[1]]).decode()).split()
    print(files)
    target_dir = sys.argv[1]
except:
    print("ERROR:  Need Target Directory")
channel_id = sys.argv[2]
if target_dir[-1] == '/':
    target_dir = target_dir[:-1]

lcount = 0 
db = dbconn('snowy')
create_channel_table(db, channel_id)
for fnum in range(len(files)):
    if fnum > 0:
        name = target_dir + "/messages" + str(fnum + 1) + ".html"
        #fil = open(target_dir + "/messages" + str(fnum + 1) + ".html")
    else:
        name = target_dir + "/messages.html"
    fil = open(name)
    page_list = html_parser_page(fil, target_dir, channel_id)
    print('page length ' + str(len(page_list)))
    print(name)
    for dd in page_list:
        lcount += 1 
        #dd = d  #.split(',')
        #dd[0] = int(dd[0]) 
        #insertquery = "insert into financial_ads(mid, cid, mtype, uname, mtime, mtxt, img_loc, links, cname) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(*dd)
        #insertquery = "insert into financial_ads(mid, cid, mtype, uname, mtime, mtxt, img_loc, links, cname) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        db.cursor.execute(insertquery.format(channel_id),(dd['mid'],dd['cid'],dd['mtype'],dd['uname'],dd['mtime'],dd['mtxt'],dd['img_loc'],dd['links'],dd['cname']))
        if lcount%1000 == 0:
            print(lcount)
            #print(fnum)
            db.conn.commit()
        #break
    db.conn.commit()

# %%
