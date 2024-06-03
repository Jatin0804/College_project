from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB

@app.route('/')
def index():
    commodities = db.commodities.find()
    return render_template('index.html', commodities=commodities)

@app.route('/commodity/<name>')
def commodity(name):
    data = db.commodity_data.find({'name': name})
    return render_template('commodity.html', name=name, data=data)

if __name__ == '__main__':
    app.run(debug=True)
