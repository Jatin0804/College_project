import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers.max_years import get_max_years
from scrapers.currency import currency_url

# CONST_DATA = "HELLO"


def com_scraper(name, url):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    #update the url
    new_url = get_max_years(url)
    new_url = currency_url(new_url)
        
    # get the new address of maximum years
    driver.get(new_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    
    records = []
    parent_table = soup.find('table', 'tblData')
    all_rows = parent_table.find_all('tr')

    
    for item in all_rows:
        try:
            temp = []
        
            all_values = item.find_all('td')
            for i in all_values:
                temp.append(i.text)

            records.append(temp)
        except:
            continue

    # Close the driver
    driver.quit()

    
    # Write records to CSV
    with open(f'files/{name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Month', 'Price', 'Change'])
        writer.writerows(records)


    # Write records to JSON
    json_records = [{key: value for key, value in zip(['Month', 'Price', 'Change'], record)} for record in records]
    with open(f'files/{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_records, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    com_scraper("Gold" ,"https://www.indexmundi.com/commodities/?commodity=gold")