from pymongo import MongoClient
import csv
from analysis.clean_homepage import clean_data

client = MongoClient(
    'mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB


def savedata(csv_file):
    csv_reader = csv.DictReader(csv_file)
    records = []

    # Print the headers for debugging
    headers = csv_reader.fieldnames
    print("CSV Headers:", headers)

    for row in csv_reader:
        record = {
            'C_Name': row['Commodity Name'],
            'Monthly_Avg': row['Monthly Avg'],
            '1_Month_Change': row['1 Month Change'],
            '12_Month_Change': row['12 Month Change'],
            'Year_Date_Change': row['Year to Date Change'],
            'URL': row['URL']
        }
        records.append(record)

    if records:
        db.clean_commodities.insert_many(records)
        print(f'Inserted {len(records)} records into MongoDB.')


def createHomeDB_clean():
    try:
        with open('files/cleaned_commodities.csv', 'r', encoding='utf-8') as csv_file:
            if "commodities" in db.list_collection_names():
                return
            db.clean_commodities.drop()
            savedata(csv_file)
    except FileNotFoundError:
        clean_data()
        with open('files/cleaned_commodities.csv', 'r', encoding='utf-8') as csv_file:
            savedata(csv_file)


if __name__ == "__main__":
    createHomeDB_clean()