from bs4 import BeautifulSoup

def message_not_service(tag):
    return tag.has_attr('class') and tag['class'].count('message') > 0 and tag['class'].count('service') == 0

def has_title(tag):
    return tag.has_attr('title')

def has_href(tag):
    return tag.has_attr('href')

def get_text_from_messagetag(mtag):
    try:
        texttag = mtag.find(class_="text")
        for br in texttag.find_all("br"):
            br.replace_with("\n")
        text = texttag.text.strip()
    except:
        text = ""
    return text