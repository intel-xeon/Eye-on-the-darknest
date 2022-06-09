import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
import time
import urllib.parse

def searchforstring(response,string,splitchar):
    s = []
    list_string = string.split(splitchar)
    for j in list_string:
        if(len(j)==0):
            continue
        for x in response.xpath('//div/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//a/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//p/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//td/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//li/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//ul/text()').extract():
            if(j.lower() in x.lower()):
                s.append(x)
    return s

def getHost(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
    


def extractLink(url,link):
    print(link)
    domain = url.split("/")[0]+'//'
    domain += getHost(url)
    
    i = link.index("href=")+0
    app = link[i:]
    i = app.index('=')+2
    app = app[i:]
    #print("APP ADESSO "+app)
    ##time.sleep(2)
    x = app.index("\"")
    uri = app[0:x]
    #print("URI:"+uri)
    #print("URI "+uri+"\nLINK: "+link)
    if(len(uri)==0):
        return
    if(uri[0]!='/'):
        domain+='/'
    if (len(getHost(uri))==0):
        #print("Ritorno: "+domain+uri)
        return domain+uri
    else:
        #print("Ritorno "+uri)
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
        for url in urls:
            self.root = getHost(url)
            print("Metodo principale root: "+self.root)
            #time.sleep(5)
            sw = True
            yield scrapy.Request(url=url, callback=self.parse,cb_kwargs=dict(radix=self.root,switch=sw))

    def parse(self, response,radix,switch):
        print(switch)
        print("Mi è arrivato: "+radix)
        print(response.url)
        #time.sleep(7)
        if(switch):
            switch = False
            u = []
            for k in self.le1.extract_links(response):
                u.append(k.url)
            links = response.xpath("//a").extract()
            for a in links:
                ur = extractLink(response.url,a)
                if (ur not in u):
                    u.append(ur)
            
            for proc in u:
                if (radix in getHost(proc)):
                    switch = True
                    print("root ("+radix+") è in proc ("+proc+") quindi setto sw su True ")
                    ##time.sleep(1)
                else:
                    switch = False
                    print("root ("+radix+") NON è in proc ("+proc+") quindi setto sw su False ")
                    #time.sleep(1)
                yield scrapy.Request(url=proc, callback=self.parse,cb_kwargs=dict(radix=radix,switch=switch))
        
        matched = searchforstring(response,self.string,self.splitchar)
        if len(matched)>0:
            yield {'url':response.url,'title': response.css('title::text').get(),'match':matched}

    
