import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def home_scraper():
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    records = []
    url = "https://www.indexmundi.com/commodities/"

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)
    parent_commodities = soup.find('table', 'tblData')
    all_commodities = parent_commodities.find_all('tr')
    # print(all_commodities)

    for item in all_commodities:
        try:
            temp = []
            a_tag = item.find('td').a
            link = a_tag.get('href')

            all_values = item.find_all('td')
            for i in all_values:
                temp.append(i.text)

            link = url + link
            temp.append(link)
            print(temp)
            records.append(temp)

        except Exception as e:
            print(f"Error processing item: {e}")
            continue

    driver.quit()

   

if __name__ == '__main__':
    home_scraper()
