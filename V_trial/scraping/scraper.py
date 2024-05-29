import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

def main():
    client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
    db = client.commodityDB
    db.commodities.drop()
    db.commodity_data.drop()

    records = []
    url = "https://www.indexmundi.com/commodities/"

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parent_commodities = soup.find('table', 'tblData')
    all_commodities = parent_commodities.find_all('tr')

    for item in all_commodities:
        try:
            temp = {}
            a_tag = item.find('td').a
            link = a_tag.get('href')

            all_values = item.find_all('td')
            temp['name'] = all_values[0].text
            temp['monthly_avg'] = all_values[1].text
            temp['month_change'] = all_values[2].text
            temp['year_change'] = all_values[3].text
            temp['ytd_change'] = all_values[4].text
            temp['url'] = url + link

            records.append(temp)
            db.commodities.insert_one(temp)
        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    for commodity in records:
        scrape_individual_commodity(db, commodity['name'], commodity['url'])
        break

    driver.quit()

def scrape_individual_commodity(db, name, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parent_table = soup.find('table', 'tblData')
    all_rows = parent_table.find_all('tr')

    for item in all_rows:
        try:
            temp = {
                'month': all_values[0].text, 
                'price': all_values[1].text, 
                'change': all_values[2].text
                }
            all_values = item.find_all('td')

            db[name].insert_one(temp)
        except Exception as e:
            print(f"Error processing row for {name}: {e}")
            continue

if __name__ == '__main__':
    main()
