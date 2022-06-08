import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
import time



def searchforstring(response,string):
    s = []
    for x in response.xpath('//div/text()').extract():
        if(string.lower() in x.lower()):
            s.append(x)
        for x in response.xpath('//a/text()').extract():
            if(string.lower() in x.lower()):
                s.append(x)
        for x in response.xpath('//p/text()').extract():
            if(string.lower() in x.lower()):
                s.append(x)
        return s


def extractLink(url,link):
    domain = url.split("/")[0]+'//'
    domain += url.split("/")[2]
    
    i = link.index("href=")+6
    app = link[i:]
    x = app.index('"')
    uri = app[i:x]

    if(len(uri)==0):
        return
    if(uri[0]!='/'):
        domain+='/'
    
    return domain+uri

class QuotesSpider(scrapy.Spider):
    string = input("Inserisci la stringa da ricercare: ")
    name = "search"
    le1 = LinkExtractor()
    rules = (Rule(le1, callback='parse_item'))
    sw = True

    
    def start_requests(self):
        urls=[]
        r = open("url.txt",'r')
        for x in r:
            if (len(x)-1=='\n'):
                urls.append(x[0:len(x)-1])
            else:
                urls.append(x)
#        urls= ['https://gtfobins.github.io/']
        for url in urls:
            sw = True
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if(self.sw):
            self.sw = False
            u = []
            for k in self.le1.extract_links(response):
                u.append(k.url)
            links = response.xpath("//a").extract()
            for a in links:
                ur = extractLink(response.url,a)
                if (ur not in u):
                    u.append(ur)
            for proc in u:
                yield scrapy.Request(url=proc, callback=self.parse)
        matched = searchforstring(response,self.string)
        if len(matched)>0:
            yield {'url':response.url,'title': response.css('title::text').get(),'match':matched}

    
