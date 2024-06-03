from pymongo import MongoClient

client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB

comm_name = db.commodities.find_one({
        "C_Name": "Gasoline"
})
print(comm_name)
url = comm_name['URL']
new_url = comm_name.get('URL')
print(url)
print(new_url)