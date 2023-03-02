import requests, re, csv
import time
import lxml.html
import sys

from bs4 import BeautifulSoup
# from lxml import etree


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}
urls = []

http_proxy = "http://adminshapegc:WWEMAXGDjht5ok7i@proxy.packetstream.io:31112"
https_proxy = "http://adminshapegc:WWEMAXGDjht5ok7i@proxy.packetstream.io:31112"
# http_proxy = "http://Adminshapegc:adminshapegcpassword@us-wa.proxymesh.com:31280"
# https_proxy = "http://Adminshapegc:adminshapegcpassword@us-wa.proxymesh.com:31280"


proxies = {
    "http": http_proxy,
    "https": https_proxy,
}

manual_pages = 9
pages = 0
main_url = 'https://www.redfin.com/city/14057/CA/Orinda/filter/include=sold-5yr'
property_urls = set()
failed_property_urls = set()

while True:
    result = requests.get(main_url, headers=header, proxies=proxies)
    tree = lxml.html.fromstring(result.content)
    pages = tree.xpath("//*[@class='clickable goToPage'][last()]/text()")[0]
    if int(manual_pages) == int(pages):
    # if True:
        break
    else:
        print("retry request")

column_header = ['Price', 'Beds', 'Baths', 'URL', 'Sqft', 'Address', 'State', 'Zip_code', 'Sold Description', 'Status']

print("There are {} pages in the options".format(pages))

for i in range(1, int(pages)+1):
    print('{}/page-{}'.format(main_url, i), '\r')
    
    try:
        results = requests.get('{}/page-{}'.format(main_url, i), headers=header, proxies=proxies)
        tree = lxml.html.fromstring(results.content)
        property_urls.update(tree.xpath("//*[@class='scrollable']/a/@href"))
        break
    except Exception as ex:
        import pdb;pdb.set_trace()
        break

with open('redfin.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(column_header)
    for property_url in property_urls:
        try:
            url = 'https://www.redfin.com{}'.format(property_url)
            result_url = ""
            try:
                result_url = requests.get(url, headers=header, proxies=proxies)
            except Exception as ex:
                result_url = requests.get(url, headers=header, proxies=proxies)

            tree = lxml.html.fromstring(result_url.content)
            overview = tree.xpath("//div[@class='statsValue']//text()")
            
            #overview
            price = overview[0]
            beds = overview[1]
            baths = overview[2]
            url_object = url
            
            # Sqft
            square_ft = tree.xpath("//*[@class='stat-block sqft-section'][1]/span/text()")[0]         
            address_object = ''. join(str(e) for e in tree.xpath("//*[@class='full-address']//text()"))
            address = address_object.split(',')[0]
            state = address_object.split(' ')[-2]
            zip_code = address_object.split(' ')[-1]
  
            sold_class = tree.xpath("//*[@class='secondary-info']/text()")[0] 
            property_status = ""
            if len(tree.xpath("//*[contains(@class, 'recently-sold')]")):
                property_status = "Recently Sold"
            else:
                property_status = "Off Market"
            
            print(property_status)
            data_to_write = [price, beds, baths, url_object, square_ft, address, state, zip_code, sold_class, property_status]
            writer.writerow(data_to_write)
        except Exception as ex:
            failed_property_urls.update(property_url)
            print(property_url)
            print(ex, "Added again in queue", property_url)

property_urls = failed_property_urls
with open('redfin.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(column_header)
    for property_url in property_urls:
        try:
            url = 'https://www.redfin.com{}'.format(property_url)
            result_url = ""
            try:
                result_url = requests.get(url, headers=header, proxies=proxies)
            except Exception as ex:
                result_url = requests.get(url, headers=header, proxies=proxies)

            tree = lxml.html.fromstring(result_url.content)
            overview = tree.xpath("//div[@class='statsValue']//text()")
            
            #overview
            price = overview[0]
            beds = overview[1]
            baths = overview[2]
            url_object = url
            
            # Sqft
            square_ft = tree.xpath("//*[@class='stat-block sqft-section'][1]/span/text()")[0]         
            address_object = ''. join(str(e) for e in tree.xpath("//*[@class='full-address']//text()"))
            address = address_object.split(',')[0]
            state = address_object.split(' ')[-2]
            zip_code = address_object.split(' ')[-1]
  
            sold_class = tree.xpath("//*[@class='secondary-info']/text()")[0] 
            property_status = ""
            if len(tree.xpath("//*[contains(@class, 'recently-sold')]")):
                property_status = "Recently Sold"
            else:
                property_status = "Off Market"
            
            print(property_status)
            data_to_write = [price, beds, baths, url_object, square_ft, address, state, zip_code, sold_class, property_status]
            writer.writerow(data_to_write)
        except Exception as ex:            
            print(ex, "Added again in queue", property_url)

print('Scraping Done Successfully')
