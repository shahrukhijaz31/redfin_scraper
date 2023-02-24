import requests, re, csv

from bs4 import BeautifulSoup


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}
urls = []

result = requests.get('https://www.redfin.com/city/2471/CA/Calabasas/filter/include=sold-5yr', headers=header)
pages_count = BeautifulSoup(result.content, 'html.parser')
for page in pages_count.find_all('a', {'class': 'clickable goToPage'})[::-7]:
    # manual verification for pages
    print(page.text.strip(),'pages')
    for i in range(1,int(page.text.strip())):
        results = requests.get('https://www.redfin.com/city/2471/CA/Calabasas/filter/include=sold-5yr/page-{}'.format(i), headers=header)
        data = BeautifulSoup(results.content, 'html.parser')
        for tag in data.find_all('div', {'class': 'scrollable'}):
            url = 'https://www.redfin.com'+tag.find('a').get('href')
            urls.append(url)
    Column_Header = ['price', 'beds', 'baths', 'URL', 'Sqft', 'Adress', 'state', 'zip_code', 'Sold Price', 'Sold Date']
    with open('redfin.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(Column_Header)

        for url in urls:
            result_url = requests.get(url, headers=header)
            soup_data_url = BeautifulSoup(result_url.content, 'html.parser')
            overview = soup_data_url.find_all('div', {'class': 'statsValue'})
            #overview
            price = overview[0].text
            beds = overview[1].text
            baths = overview[2].text
            URL = url
            # Sqft
            square_foot = soup_data_url.find_all('div', {'class': 'stat-block sqft-section'})
            Square_ft = square_foot[0].text
            adress = soup_data_url.find_all('div', {'class': 'homeAddress'})
            Adress = adress[0].text
            state = adress[0].text.split(' ')[-2]
            zip_code = adress[0].text.split(' ')[-1]
            sold_class = soup_data_url.find_all('div', {'class': 'secondary-info'})
            if sold_class[0].text.split(' ')[5] != 'ago.':
                SOLD = sold_class[0].text.split(' ')[5]
            else:
                SOLD = ' '
            date = soup_data_url.find_all('div', {'class': 'secondary-info'})
            DATE = date[0].text.split(' ')[-3]+' '+date[0].text.split(' ')[-2]+date[0].text.split(' ')[-1]
            data_to_write = [price, beds, baths, URL, Square_ft, Adress, state, zip_code, SOLD, DATE]
            writer.writerow(data_to_write)
        break
    break

print('ok')