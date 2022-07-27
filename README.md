
<a href="https://www.instagram.com/luke_fireeye_1996/
" ><img src="https://img.shields.io/badge/@luke__fireeye__1996-Instragram-blue" /> </a><img src="https://img.shields.io/badge/Tested on Python-3.8%20%7C%203.10-00e600.svg" />
<img src="https://img.shields.io/badge/dark%20web-clearnet-blue" />
# Eye on the darknest

Eye on the darknest helps you find valuable information on the web. <br><br>Based on keyword search, it searches a set of urls for the keywords you want. For each url provided, Eye on the darknest searches for keywords recursively in the links in the same. 


<h3> Install dependencies</h3>

<pre class="notranslate">
<code> pip3 install Scrapy</code>
</pre>

<pre class="notranslate">
<code> apt-get install tor -y</code>
</pre>

<h3> preliminary steps </h3>

<pre class="notranslate">
<code>git clone https://github.com/intel-xeon/crawler.git</code>
</pre>

<pre class="notranslate">
<code>cd Eye-on-the-darknest/scrapy/crawler/crawler/</code>
</pre>

<h3>>_ CLI interface:</h3>

![image](https://user-images.githubusercontent.com/37773731/177152604-67b5b833-8ab7-4e69-8ca6-582f115b6f5d.png)

<h3>Templates:</h3>

Use proposed default templates or create your own!

![image](https://user-images.githubusercontent.com/37773731/178488222-89eaff13-e669-451e-a7d8-6235319198fa.png)

<h3> usage example (clearnet): </h3>


<pre class="notranslate">
<code>python3 controller.py --file url.txt --query "Jane" --splitter "/" --onlyscope --path /var/www/html/</code>
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
<code>python3 controller.py --file url.txt --query "Jane" --splitter "/" --onlyscope --path /var/www/html/ <strong>--tor</strong></code>
</pre>

<h3> usage example with templates: </h3>

To see the available templates type:

<pre class="notranslate">
<code>python3 controller.py -l</code>
</pre>

![image](https://user-images.githubusercontent.com/37773731/178488222-89eaff13-e669-451e-a7d8-6235319198fa.png)

Search for IPv4 and email example:
<pre class="notranslate">
<code>python3 controller.py --file url.txt -z 1,6 --path /var/www/html</code>
</pre>

<h3> usage example (RegEx): </h3>


<pre class="notranslate">
<code>python3 controller.py --file url.txt --query "[YOUR_REGEX_1]@@[YOUR_REGEX_2]" --splitter "@@" --onlyscope --path /var/www/html/ -x 1,2</code>
</pre>

<h3> Recursive </h3>


Do not specify all URLs within a site. Pass a single URL and let Eye on the darknest scan him all the links there!

![image](https://user-images.githubusercontent.com/37773731/174990876-6b5b1850-5b74-48c9-9a75-da779906360c.png)

<h3> Export data in JSON </h3>

Import data where and how you want thanks to export in JSON format

![image](https://user-images.githubusercontent.com/37773731/174990596-5c2c2ead-4233-4895-8f04-775550f5e147.png)

<h3>Generate automated HTML datatable of your keywords</h3>

![image](https://user-images.githubusercontent.com/37773731/181294607-01d99e36-1bde-4364-ab22-2a96c69b87fd.png)

<h3>you can find lists of .onion sites here:</h3>

<ul>
  <li> Hunchly https://www.hunch.ly/darkweb-osint/</li>
  <li>Darknet.fail https://darknet.fail/</li>
  <li>Tor66 http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/fresh</li>
</ul> 
 



<h3> Recommended users: </h3>

1. Law enforcement
2. Federal agents
3. Cyber Security Threat Intelligence Analyst
4. Undercover agents

