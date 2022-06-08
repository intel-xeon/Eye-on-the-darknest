import scrapy
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor

class QuotesSpider(scrapy.Spider):
    name = "title"
    le1 = LinkExtractor()
    rules = (Rule(le1, callback='parse_item'))

    def start_requests(self):
        urls = ['https://google.it']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for x in self.le1.extract_links(response):
            proc = x.url
            yield scrapy.Request(url=proc, callback=self.parse)
        #match = response.css('body').re('(\W|^)[\w.\-]{0,25}@(yahoo|hotmail|gmail)\.com(\W|$)')
        match = response.css('body').re('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')
        if len(match)>0:
            yield {'url':response.url,'title': response.css('title::text').get(),'match':match}
