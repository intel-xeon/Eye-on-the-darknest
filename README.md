<a href="https://www.instagram.com/luke_fireeye_1996/?hl=bn
" ><img src="https://img.shields.io/badge/@luke__fireeye__1996-Instragram-blue" /> </a><img src="https://img.shields.io/badge/Python-3.8%20%7C%203.10-00e600.svg" />

# Web crawler

# Install dependencies

<pre class="notranslate">
<code> pip3 install Scrapy</code>
</pre>

# preliminary steps 

<pre class="notranslate">
<code>git clone https://github.com/intel-xeon/crawler.git</code>
</pre>

<pre class="notranslate">
<code>cd crawler/scrapy/crawler/crawler/</code>
</pre>

# usage example (clearnet):


<pre class="notranslate">
<code>scrapy  crawl search  -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/</code>
</pre>

result saved in "result.json"


# usage example (dark web):


<pre class="notranslate">
<code>apt-get install tor -y</code>
</pre>
<pre class="notranslate">
<code>/etc/init.d/tor start</code>
</pre>

3. check that you have port 9050 opened with command: <br>
<pre class="notranslate">
<code>netstat -plnt</code>
</pre>
<pre class="notranslate">
<code>torify scrapy  crawl search -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/</code>
</pre>


# Recommended users:

1. Law enforcement
2. Federal agents
3. Cyber Security Threat Intelligence Analyst
4. Undercover agents

<br><br>Author: Luca Marsilia
