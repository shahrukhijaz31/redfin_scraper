
import requests, re, csv
import time
import lxml.html
import sys


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}

http_proxy = "http://adminshapegc:WWEMAXGDjht5ok7i@proxy.packetstream.io:31112"
https_proxy = "http://adminshapegc:WWEMAXGDjht5ok7i@proxy.packetstream.io:31112"
# http_proxy = "http://Adminshapegc:adminshapegcpassword@us-wa.proxymesh.com:31280"
# https_proxy = "http://Adminshapegc:adminshapegcpassword@us-wa.proxymesh.com:31280"


proxies = {
    "http": http_proxy,
    "https": https_proxy,
}

main_url = 'https://apps.shopify.com/search?q=b&page=1'

results = requests.get(main_url, headers=header, proxies=proxies)
tree = lxml.html.fromstring(results.content)

f = open("demofile2.html", "w")
f.write(results.text)
f.close()
import pdb;pdb.set_trace()
pages = tree.xpath("//div[@aria-label='pagination']/a")
print(pages)