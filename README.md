# crawler

#installation:

pip3 install Scrapy

#usage example (clearnet):

1. git clone https://github.com/intel-xeon/crawler.git
2. cd  crawler/scrapy/crawler/crawler/
3. scrapy  crawl search  -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/ 
4. result saved in "result.json"


If you want use this for search in the dark net:

1. apt-get install tor -y
2. /etc/init.d/tor start
3. check that you have port 9050 opened with command: netstat -plnt
4. torify scrapy  crawl search -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/


Recommended users:

Law enforcement
Federal agents
Cyber Security Threat Intelligence Analyst
Undercover agents
