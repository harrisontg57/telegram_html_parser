import sys
import subprocess
from bs4 import BeautifulSoup
import csv
from tag_lambdas import message_not_service, has_title, has_href, get_text_from_messagetag

target_dir = sys.argv[1]
try:
    #needs error catching for folder
    files = (subprocess.check_output(['ls', sys.argv[1]]).decode()).split()
    print(files)
    target_dir = sys.argv[1]
except:
    print("ERROR:  Need Target Directory")

if target_dir[-1] == '/':
    target_dir = target_dir[:-1]



values_list = []
line_count = 0
#Iterate in order by going in range 0 to len(files)
for fnum in range(len(files)):
    if fnum > 0:
        fil = open(target_dir + "/messages" + str(fnum + 1) + ".html")
    else:
        fil = open(target_dir + "/messages.html")
    html_doc = fil.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    mydivs = soup.findAll(message_not_service)
    texts = []
    c = 0
    for x in mydivs:
        hasImg = None
        hasLink = False
        joined = False
        nameDiv = x.find("div", {"class": "from_name"})
        textDiv = x.find("div", {"class": "text"})
        mediaDiv = x.find("div", {"class": "media_wrap"})
        #print(mediaDiv)
        titleDiv = x.findAll(has_title)
        time = titleDiv[0]['title']
        mnum = c #Fix THIS
        c += 1

        if mediaDiv:
            im = mediaDiv.find("a", {"class": "photo_wrap"})
            if im:
                hasImg = im['href']
        #title extract goes here
        if nameDiv:  #find() returns None if the query is not found
            nameTemp = nameDiv.contents[0]
            name = nameTemp.strip()
            #print(name)
        else:
            #names.append(None)
            name = ''
            joined = True

        if textDiv and textDiv.string is not None:
            temp = textDiv.string[1:]
            texts.append(temp[:-8])
            #text = temp[:-8]
            text = temp.strip()
        elif textDiv:
            text = get_text_from_messagetag(textDiv)
            links = textDiv("a")
            if len(links) > 0:
                hasLink = True
        else:
            text = ""
            
        values_list.append({'mid':mnum, 'name':name.strip(), 'text':text, 'time':time, 'joined':joined, 'image':hasImg, 'link':hasLink})

    line_count += len(texts)
    print(str(len(texts)))


print("Total Lines of Chat:  " + str(line_count))
#values_list = values_list[1:]
with open(target_dir + '.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, 
                        fieldnames=values_list[0].keys(),

                       )
    fc.writeheader()
    fc.writerows(values_list)