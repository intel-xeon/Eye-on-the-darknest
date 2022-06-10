# crawler

#installation:

pip3 install Scrapy

#usage example:

1. git clone https://github.com/intel-xeon/crawler.git
2. cd  crawler/scrapy/crawler/crawler/
3. scrapy  crawl search  -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/ 
4. result saved in "result.json"
