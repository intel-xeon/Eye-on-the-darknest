import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
import time
import urllib.parse
import unicodedata
from scrapy.exporters import JsonItemExporter
import html



def testmultiple(q,stringa):
    app = 0
    for x in q.split("*"):
        if (x in stringa):
            app = stringa.index(x)+len(x)
            stringa = stringa[app:]
        else:
            return False
    return True

def writereport(lista):
    w = "{\"data\":["
    for x in lista:
        k = str(x).replace("'",'"')
        w+=k
        w+=","
    w = w[0:len(w)-1]
    w+="]}"
    f = open("/var/www/html/out/nuovo.json", "w")
    f.write(str(w))
    f.close()



def searchforstring(response,string,url):
    element = ['a','abbr','acronym','address','applet','area','article','aside','audio','b','base','basefont','bdi','bdo','bgsound','big','blink','blockquote','body','br','button','canvas','caption','center','circle','cite','clipPath','code','col','colgroup','command','content','data','datalist','dd','defs','del','details','dfn','dialog','dir','div','dl','dt','element','ellipse','em','embed','fieldset','figcaption','figure','font','footer','foreignObject','form','frame','frameset','g','h1','h2','h3','h4','h5','h6','head','header','hgroup','hr','html','i','iframe','image','img','input','ins','isindex','kbd','keygen','label','legend','li','line','linearGradient','link','listing','main','map','mark','marquee','mask','math','menu','menuitem','meta','meter','multicol','nav','nextid','nobr','noembed','noframes','noscript','object','ol','optgroup','option','output','p','param','path','pattern','picture','plaintext','polygon','polyline','pre','progress','q','radialGradient','rb','rbc','rect','rp','rt','rtc','ruby','s','samp','script','section','select','shadow','slot','small','source','spacer','span','stop','strike','strong','style','sub','summary','sup','svg','table','tbody','td','template','text','textarea','tfoot','th','thead','time','title','tr','track','tspan','tt','u','ul','var','video','wbr','xmp']
    match = []
    for e in element:
        try:
            for x in response.xpath('//'+e+'/text()').extract():
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
        except Exception:
            continue
        if (len(match)==0):
            continue
    
    return {"url":url, "matched":match}

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

def existKey(key,list_json):
    for x in list_json:
        if(x["key"]==html.escape(key)):
            return True
    return False
    

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
        if (len(self.splitchar)==0):
            print ("Sorry.. you must specify splitchar exit..")
            time.sleep(3)
            return
            
        urls=[]
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
            yield scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(radix=self.root,switch=sw,list_json=self.list_json))

    def parse(self, response,radix,switch,list_json):
        try:
            self.onlyscope
        except Exception:
            self.onlyscope = 'no'
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
            for x in u:
                print(x)
            for proc in u:
                if (radix in getHost(proc)):
                    switch = True
                else:
                    switch = False
                yield scrapy.Request(url=proc, callback=self.parse,cb_kwargs=dict(radix=radix,switch=switch,list_json=list_json))
        
        list_string = self.string.split(self.splitchar)
        for x in list_string:
            if (len(x)==0):
                continue
            matched = searchforstring(response,x,response.url)
            if len(matched["matched"])>0:
                if (existKey(x,list_json)==False):
                    list_json.append({'key':html.escape(x),'title': html.escape(response.css('title::text').get()),'matched':[matched]})
                    writereport(list_json)
                else:
                    i = 0
                    for k in list_json:
                        if(k["key"]==x):
                            list_json[i]["matched"].append(matched)
                            break
                        i+=1
                    writereport(list_json)


                            
