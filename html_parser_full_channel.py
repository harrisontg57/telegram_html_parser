import sys
import subprocess
from bs4 import BeautifulSoup
import csv
from tag_lambdas import message_not_service, has_title, has_href, get_text_from_messagetag
import re

#target_dir = sys.argv[1]


#print(target_dir)



#Iterate in order by going in range 0 to len(files)
def html_parser_page(fil, target_dir, cid):
    values_list = []
    line_count = 0
    html_doc = fil.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    mydivs = soup.findAll(message_not_service)
    #print('mydivs ' + str(len(mydivs)))
    texts = []
    c = 0
    for x in mydivs:
        hasImg = None
        hasLink = None
        joined = 0
        nameDiv = x.find("div", {"class": "from_name"})
        textDiv = x.find("div", {"class": "text"})
        mediaDiv = x.find("div", {"class": "media_wrap"})
        #print(mediaDiv)
        titleDiv = x.findAll(has_title)
        time = titleDiv[0]['title']
        mnum = c #Fix THIS
        c += 1

        if mediaDiv:
            im = mediaDiv.findAll("a", {"class": "photo_wrap"})
            if len(im) > 0:
                hasImg = str(im[0]['href'])
            if len(im) > 1:
                for x in im[1:]:
                    hasImg = hasImg + "," + x['href']
            
        #title (Time) extract goes here
        if nameDiv:  #find() returns None if the query is not found
            nameTemp = nameDiv.contents[0]
            name = nameTemp.strip()
            #print(name)
        else:
            #names.append(None)
            name = ''
            joined = 1

        if textDiv and textDiv.string is not None:
            temp = textDiv.string[1:]
            texts.append(temp[:-8])
            #text = temp[:-8]
            text = temp.strip()
        elif textDiv:
            text = get_text_from_messagetag(textDiv)
            links = textDiv("a")
            if len(links) > 0:
                hasLink = links[0]['href']
            if len(links) > 1:
                for xx in links[1:]:
                    hasLink = hasLink + "," + xx['href']
        else:
            text = ""
            
        name = name.strip()
        name = name.replace(",",'')
        values_list.append({'mid':mnum,'cid':cid, 'mtype':joined, 'uname':name, 'mtime':time, 'mtxt':text, 'img_loc':hasImg, 'links':hasLink, 'cname':target_dir})
    return values_list
    #line_count += len(texts)
    #print(str(len(texts)))


#print("Total Lines of Chat:  " + str(line_count))
#values_list = values_list[1:]
def make_csv(values_list, target_dir):
    with open(target_dir + '.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, 
                            fieldnames=values_list[0].keys(),

                        )
        fc.writeheader()
        fc.writerows(values_list)