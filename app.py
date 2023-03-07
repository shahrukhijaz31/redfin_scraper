import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

links = []
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

main_url = "https://apps.shopify.com/search?q=z&page={}"
driver.get(main_url.format(1))
time.sleep(5)


pages = int(driver.find_element(By.XPATH, '//a[contains(text(),"Next")]/preceding-sibling::a[1]').text)
print("Total number of pages {}".format(pages))

for page in range(1, pages+1):  
    print(page)
    time.sleep(5)
    count = len(driver.find_elements(By.XPATH, '//a[@data-app-link-details]'))  
    if count == 0:
        import pdb;pdb.set_trace()
    
    print("App found {}".format(count))
    for application in driver.find_elements(By.XPATH, '//a[@data-app-link-details]'):
        links.append(application.get_attribute('href'))
    
    time.sleep(7)

    driver.get((main_url.format(page)))

    print("Scraped links are {}".format(len(links)))

json_object = json.dumps(links, indent=4)

with open("z_cat.json", "w") as outfile:
    outfile.write(json_object)
print("ok")

