from pymongo import MongoClient
import csv
from scrapers.commodity_scraper import com_scraper

# MongoDB connection
client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB

def savedata(csv_file, name):
    csv_reader = csv.DictReader(csv_file)
    records = []

    # Print the headers for debugging
    headers = csv_reader.fieldnames
    print("CSV Headers:", headers)

    for row in csv_reader:
        record = {
            'name': name,
            'Month': row['Month'],
            'Price': row['Price'],
            'Change': row['Change']
        }
        records.append(record)

    if records:
        db[name].insert_many(records)
        print(f'Inserted {len(records)} records into MongoDB collection: {name}')


def createComDB(name, url):

    try:
        with open('../files/Gold.csv', 'r', encoding='utf-8') as csv_file:
            savedata(csv_file, name)

    except FileNotFoundError:
        com_scraper(name, url)
        with open('../files/Gold.csv', 'r', encoding='utf-8') as csv_file:
            savedata(csv_file, name)

if __name__ == "__main__":
    createComDB("Gold", "https://www.indexmundi.com/commodities/?commodity=gold")

    # try :
    #     with open('V5/files/Silver.csv', 'r', encoding='utf-8') as csv_file:
    #         print("file exists")
    #
    # except FileNotFoundError:
    #     # print(e)
    #     print("file doesnot exist")
        
