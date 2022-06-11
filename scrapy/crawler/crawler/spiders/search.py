import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
import time
import urllib.parse
import getopt
import sys
from scrapy.exporters import JsonItemExporter


def testmultiple(q,stringa):
    app = 0
    for x in q.split("*"):
        if (x in stringa):
            app = stringa.index(x)+len(x)
            stringa = stringa[app:]
        else:
            return False
    print("Sto per dare true qui q:"+q+" stringa:"+stringa)
    return True



def searchforstring(response,string,splitchar):
    #element = ["div","a","p","td","li","ul","small"]
    element = ['a','abbr','acronym','address','applet','area','article','aside','audio','b','base','basefont','bdi','bdo','bgsound','big','blink','blockquote','body','br','button','canvas','caption','center','circle','cite','clipPath','code','col','colgroup','command','content','data','datalist','dd','defs','del','details','dfn','dialog','dir','div','dl','dt','element','ellipse','em','embed','fieldset','figcaption','figure','font','footer','foreignObject','form','frame','frameset','g','h1','h2','h3','h4','h5','h6','head','header','hgroup','hr','html','i','iframe','image','img','input','ins','isindex','kbd','keygen','label','legend','li','line','linearGradient','link','listing','main','map','mark','marquee','mask','math','menu','menuitem','meta','meter','multicol','nav','nextid','nobr','noembed','noframes','noscript','object','ol','optgroup','option','output','p','param','path','pattern','picture','plaintext','polygon','polyline','pre','progress','q','radialGradient','rb','rbc','rect','rp','rt','rtc','ruby','s','samp','script','section','select','shadow','slot','small','source','spacer','span','stop','strike','strong','style','sub','summary','sup','svg','table','tbody','td','template','text','textarea','tfoot','th','thead','time','title','tr','track','tspan','tt','u','ul','var','video','wbr','xmp']
    s = {}
    list_string = string.split(splitchar)
    for j in list_string:
        if(len(j)==0):
            continue
        s[j]=[]
        for e in element:
            try:
                for x in response.xpath('//'+e+'/text()').extract():
                    if("*" in j):
                        if(testmultiple(j.lower(),x.lower())):
                            s[j].append(x)
                    else:
                        if(j.lower() in x.lower()):
                            s[j].append(x)
            except Exception:
                continue
        if (len(s[j])==0):
            s.pop(j)
    return s

def getHost(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
    


def extractLink(url,link):
    #print(link)
    domain = url.split("/")[0]+'//'
    domain += getHost(url)
    try:
        i = link.index("href=")+0
    except Exception:
        return ""
    app = link[i:]
    i = app.index('=')+2
    app = app[i:]
    ##print("APP ADESSO "+app)
    ##time.sleep(2)
    x = app.index("\"")
    uri = app[0:x]
    ##print("URI:"+uri)
    ##print("URI "+uri+"\nLINK: "+link)
    if(len(uri)==0):
        return
    if(uri[0]!='/'):
        domain+='/'
    if (len(getHost(uri))==0):
        ##print("Ritorno: "+domain+uri)
        return domain+uri
    else:
        ##print("Ritorno "+uri)
        return uri





class searchSpider(scrapy.Spider):
    
    urls=[]
    splitchar = ""
    string = ""
    def __init__(self, *args, **kwargs):
        super(searchSpider, self).__init__(*args, **kwargs)

            
    
    #splitchar = input("Inserisci un separatore di stringhe: ")
    #string = input("Inserisci la stringa da ricercare (per separare più stringhe utilizzare il separatore '"+splitchar+"' ): ")
    #time.sleep(10)
    name = "search"
    le1 = LinkExtractor()
    rules = (Rule(le1, callback='parse_item'))
    sw = True
    root = ""
    list_json=[]
    
    def start_requests(self):
        urls=[]
        r = open(self.file,'r')
        for x in r:
            if (not x.startswith("http")):
                x = "http://"+x
            if (len(x)-1=='\n'):
                urls.append(x[0:len(x)-1])
            else:
                urls.append(x)
     #  urls = ["https://quotes.toscrape.com/page/1/","https://quotes.toscrape.com/page/2/"]
        for url in urls:
            self.root = getHost(url)
            #print("Metodo principale root: "+self.root)
            #time.sleep(5)
            sw = True
            yield scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(radix=self.root,switch=sw,list_json=self.list_json))

    def parse(self, response,radix,switch,list_json):
        #print(switch)
        #print("Mi è arrivato: "+radix)
        #print(response.url)
        #time.sleep(7)
        if(switch):
            switch = False
            u = []
            for k in self.le1.extract_links(response):
                u.append(k.url)
            links = response.xpath("//a").extract()
            for a in links:
                ur = extractLink(response.url,a)
                if ur is not None:
                    if (ur not in u and len(ur)>0):
                        u.append(ur)
           # print("\n\n\n\n\n\n")
            for x in u:
                print(x)
            #print("\n\n\n\n\n\n")
            #time.sleep(9)
            for proc in u:
                if (radix in getHost(proc)):
                    switch = True
                    #print("root ("+radix+") è in proc ("+proc+") quindi setto sw su True ")
                    ##time.sleep(1)
                else:
                    switch = False
                    #print("root ("+radix+") NON è in proc ("+proc+") quindi setto sw su False ")
                    #time.sleep(1)
                yield scrapy.Request(url=proc, callback=self.parse,cb_kwargs=dict(radix=radix,switch=switch,list_json=list_json))
        
        matched = searchforstring(response,self.string,self.splitchar)
        if len(matched)>0:
            list_json.append({'url':response.url,'title': response.css('title::text').get(),'match':matched})
            f = open("result.json", "w")
            f.write(str(list_json))
            f.close()

        #    yield {'url':response.url,'title': response.css('title::text').get(),'match':matched}
        

    
