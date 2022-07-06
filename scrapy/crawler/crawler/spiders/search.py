import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
import time
import urllib.parse
import unicodedata
from scrapy.exporters import JsonItemExporter
import html
import os
import re
import w3lib.html
import json
import ast

def testmultiple(q,stringa):
    app = 0
    for x in q.split("*"):
        if (x in stringa):
            app = stringa.index(x)+len(x)
            stringa = stringa[app:]
        else:
            return False
    return True



def writereport(lista,path):
    w = "{\"data\":["
    for x in lista:
        k = json.dumps(x)
        w+=k
        w+=","
    w = w[0:len(w)-1]
    w+="]}"
    temp = open("result/index.html",'r')
    html = open(path+"index.html","w")
    f = open(path+"result.json", "w")
    html.write(temp.read())
    temp = open("result/other.html",'r')
    html = open(path+"other.html","w")
    html.write(temp.read())
    temp = open("result/filter.html",'r')
    html = open(path+"filter.html","w")
    html.write(temp.read())
    w = json.loads(w)
    w = json.dumps(w, indent=4, sort_keys=True)
    f.write(str(w))
    f.close()
    temp.close()
    html.close()


def matchregex(string,response):
    result = []
    r = response.css('body').get()
    r = w3lib.html.remove_tags(r)
    r = r.split("\n")
    for x in r:
        m = re.finditer(string,x)
        for j in m:
            j = html.escape(j.group())
            j = unicodedata.normalize("NFKD", j)
            result.append(j)
    return result

def searchforstring(response,string,url,title,regex,index):
    element = ['a','abbr','acronym','address','applet','area','article','aside','audio','b','base','basefont','bdi','bdo','bgsound','big','blink','blockquote','body','br','button','canvas','caption','center','circle','cite','clipPath','code','col','colgroup','command','content','data','datalist','dd','defs','del','details','dfn','dialog','dir','div','dl','dt','element','ellipse','em','embed','fieldset','figcaption','figure','font','footer','foreignObject','form','frame','frameset','g','h1','h2','h3','h4','h5','h6','head','header','hgroup','hr','html','i','iframe','image','img','input','ins','isindex','kbd','keygen','label','legend','li','line','linearGradient','link','listing','main','map','mark','marquee','mask','math','menu','menuitem','meta','meter','multicol','nav','nextid','nobr','noembed','noframes','noscript','object','ol','optgroup','option','output','p','param','path','pattern','picture','plaintext','polygon','polyline','pre','progress','q','radialGradient','rb','rbc','rect','rp','rt','rtc','ruby','s','samp','script','section','select','shadow','slot','small','source','spacer','span','stop','strike','strong','style','sub','summary','sup','svg','table','tbody','td','template','text','textarea','tfoot','th','thead','time','title','tr','track','tspan','tt','u','ul','var','video','wbr','xmp']
    match = []
    if(index in regex):
        result = matchregex(string,response)
        for x in result:
            match.append(x)
        match = list(set(match))
        return {"url":url,"title":html.escape(title),"matched":match}
    for e in element:
        try:
            for x in response.xpath('//'+e+'/text()').extract():
                if (index not in regex):
                    if("*" in string):
                        if(testmultiple(string.lower(),x.lower())):
                            x = html.escape(x)
                            x = unicodedata.normalize("NFKD", x) # serve per pulire carattere sporco \xa0
                            match.append(x)
                    else:
                        if(string.lower() in x.lower()):
                            x = html.escape(x)
                            x = unicodedata.normalize("NFKD", x) # serve per pulire carattere sporco \xa0
                            match.append(x)
                #else:
                    #stringa = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        except Exception:
            continue
        if (len(match)==0):
            continue
    match = list(set(match))
    return {"url":url,"title":html.escape(title),"matched":match}

def getHost(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
    


def extractLink(url,link):
    domain = url.split("/")[0]+'//'
    domain += getHost(url)
    try:
        i = link.index("href=")+0
    except Exception:
        return ""
    app = link[i:]
    i = app.index('=')+2
    app = app[i:]
    x = app.index("\"")
    uri = app[0:x]
    if(len(uri)==0):
        return
    if(uri[0]!='/'):
        domain+='/'
    if (len(getHost(uri))==0):
        return domain+uri
    else:
        return uri

def checkname(regex):
    f = open("template.txt",'r')
    r = ast.literal_eval(f.read())
    f.close()
    for x in r:
        if(r[x]==regex):
            return x
    return regex
    


def existKey(key,list_json):
    for x in list_json:
        if(x["key"]==html.escape(key)):
            return True
    return False
    
def readtemplate(template):
     f = open("template.txt",'r')
     r = ast.literal_eval(f.read())
     f.close()
     h = template.split(",")
     i = 0
     list_string = []
     for x in r:
         i+=1
         if(str(i) in h):
             list_string.append(r[x])
     regex = ""
     for x in range(len(list_string)):
         x+=1
         regex+=str(x)+","
     return (list_string,regex[0:len(regex)-1])

class searchSpider(scrapy.Spider):
    
    urls=[]
    splitchar = ""
    string = ""
    def __init__(self, *args, **kwargs):
        super(searchSpider, self).__init__(*args, **kwargs)
    name = "search"
    le1 = LinkExtractor()
    rules = (Rule(le1, callback='parse_item'))
    sw = True
    root = ""
    list_json=[]
    
    def start_requests(self):
        try:
            self.regex = self.regex.split(",")
        except Exception:
            self.regex = [-1]
        try:
            self.splitchar
        except Exception:
            self.splitchar = -1
        urls=[]
        list_string = []
        try:
            l_string,self.regex = readtemplate(self.template)
        except Exception:
            l_string = self.string.split(self.splitchar)
        r = open(self.file,'r')
        for x in r:
            if (not x.startswith("http")):
                x = "http://"+x
            if (len(x)-1=='\n'):
                urls.append(x[0:len(x)-1])
            else:
                urls.append(x)
        for url in urls:
            self.root = getHost(url)
            sw = True
            yield scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(radix=self.root,switch=sw,list_json=self.list_json,regex=self.regex,list_string=l_string))

    def parse(self, response,radix,switch,list_json,regex,list_string):
        try:
            self.onlyscope
        except Exception:
            self.onlyscope = 'no'
        try:
            self.path
        except Exception:
            self.path = ''
        #if(len(self.path)>0):
            #self.path = validatepath(self.path)
        if(switch):
            switch = False
            u = []
            for k in self.le1.extract_links(response):
                if(self.onlyscope.lower()=='yes'):
                    if(radix not in k.url):
                        continue
                print(k.url)
                u.append(k.url)
            links = response.xpath("//a").extract()
            for a in links:
                ur = extractLink(response.url,a)
                if ur is not None:
                    if(self.onlyscope.lower()=='yes'):
                        if(radix not in a):
                            continue
                    print(ur)
                    if (ur not in u and len(ur)>0):
                        u.append(ur)
            for proc in u:
                if (radix in getHost(proc)):
                    switch = True
                else:
                    switch = False
                yield scrapy.Request(url=proc, callback=self.parse,cb_kwargs=dict(radix=radix,switch=switch,list_json=list_json,regex=regex,list_string=list_string))
        
        h = 0
        for x in list_string:
            h+=1
            if (len(x)==0):
                continue
            matched = searchforstring(response,x,response.url,str(response.css('title::text').get()),regex,str(h))
            x = html.escape(checkname(x))
            if len(matched["matched"])>0:
                if (existKey(x,list_json)==False):
                    list_json.append({'key':x,'matched':[matched]})
                    writereport(list_json,self.path)
                else:
                    i = 0
                    for k in list_json:
                        if(k["key"]==x):
                            list_json[i]["matched"].append(matched)
                            break
                        i+=1
                    writereport(list_json,self.path)
