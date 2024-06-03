import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

def get_url():
    template = 'https://www.indexmundi.com/commodities/?commodity=gold'
    url = template + "&months=240&currency=inr"
    return url

def main():

    records = []
    url = get_url()

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    with open(f'gold.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Month', 'Price', 'Change'])
        writer.writerows(records)


    # Write records to JSON
    json_records = [{key: value for key, value in zip(['Month', 'Price', 'Change'], record)} for record in records]
    with open(f'gold.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_records, json_file, ensure_ascii=False, indent=4)

main()