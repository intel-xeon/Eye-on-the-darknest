<a href="https://www.instagram.com/luke_fireeye_1996/?hl=bn
" ><img src="https://img.shields.io/badge/@luke__fireeye__1996-Instragram-blue" /> </a><img src="https://img.shields.io/badge/Python-3.8%20%7C%203.10-00e600.svg" />
<img src="https://img.shields.io/badge/dark%20web-clearnet-blue" />
# Eye on the darknest

Eye on the darknest which helps you find valuable information on the web. Based on keyword search, it searches a set of urls for the keywords you want. For each url provided, Eye on the darknest searches for keywords recursively in the links in the same. 

<h3> Install dependencies</h3>

<pre class="notranslate">
<code> pip3 install Scrapy</code>
</pre>

<h3> preliminary steps </h3>

<pre class="notranslate">
<code>git clone https://github.com/intel-xeon/crawler.git</code>
</pre>

<pre class="notranslate">
<code>cd Eye-on-the-darknest/scrapy/crawler/crawler/</code>
</pre>

<h3> usage example (clearnet): </h3>


<pre class="notranslate">
<code>scrapy  crawl search  -a file=path/of/my/url.txt -a string="String1/String2/String3/String4_part1\*String4_part2" -a splitchar=/</code>
</pre>

result saved in "result.json"


<h3> usage example (dark web): </h3>


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

<h3> Export data in JSON </h3>

Import data where and how you want thanks to export in JSON format

![image](https://user-images.githubusercontent.com/37773731/173086355-33c0b2e8-5c6b-432a-aad2-771ac86cf554.png)

<h3>You can find a list of onion site here:</h3>

<ul>
  <li> Hunchly https://www.hunch.ly/darkweb-osint/</li>
  <li>H-Indexer http://jncyepk6zbnosf4p.onion/onions.html</li>
  <li>Tor66 http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/fresh
</li>
</ul> 
 


<h3> Recommended users: </h3>

1. Law enforcement
2. Federal agents
3. Cyber Security Threat Intelligence Analyst
4. Undercover agents


<br><br>Author: Luca Marsilia
