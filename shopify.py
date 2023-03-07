import requests, re, csv
import time
import json
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

def get_scraped_page(main_url):
    results = requests.get(main_url, headers=header, proxies=proxies)
    tree = lxml.html.fromstring(results.content)

    product_description = tree.xpath('//div[@id="app-details"]//text()')
    product_description = ' '.join([str(elem.strip()) for elem in product_description])

    product_description = product_description.replace('"', '\\"')
    product_description = product_description.replace("'", "\\'")

    product_name = tree.xpath('//meta[@property="og:title"]/@content')[0].strip().split("-")[0]
    # print("product name")

    rating =  tree.xpath('//span[contains(text(), "Rating")]/text()')[0].strip()
    # print("product rating")
    
    reviews = tree.xpath('//*[text()="Reviews"]/following-sibling::div/a/text()')[0].strip()
    # print("product reviews")

    launched_date = tree.xpath('//p[contains(text(),"Launched")] /following-sibling::p/text()')[0].strip()
    # print("product launched date")

    categories = ', '.join( [category.strip() for category in tree.xpath('//p[contains(text(),"Categories")] /following-sibling::span/a/text()')])
    # print("product categories")

    support_email = tree.xpath('//span[contains(text(), "Send a message")]/following-sibling::p/text()')[0].strip()
    # print("product support email")

    return [product_name, product_description, rating, reviews, launched_date, categories, support_email]

main_url = 'https://apps.shopify.com/dsers?surface_detail=finding-products-product-sourcing-dropshipping&surface_inter_position=2&surface_intra_position=1&surface_type=category&surface_version=redesign'

column_header = ['Name', 'Description', 'Rating', 'Reviews', 'Launched Date', 'Categories', 'Support Email']


f = open('A_cat.json')
urls = json.load(f)

with open('output/cat_a.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_header)
    for url in urls:
        try:
            data_to_write = get_scraped_page(url)
            writer.writerow(data_to_write)
            print("DONE")
        except Exception as ex:
            # import pdb;pdb.set_trace()
            print("data failed ", url)
        time.sleep(10)
f.close()

