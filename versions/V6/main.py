import datetime
import time
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from pymongo import MongoClient

# install database packages
from database.createDB_home import createHomeDB
from database.createDB_commodity import createComDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB


# Function to update the home page data if necessary
def getHomePage():
    last_update = db.metadata.find_one({"type": "home_update"})
    if not last_update or (datetime.datetime.now() - last_update['timestamp']).total_seconds() > 86400:
        createHomeDB()
        db.metadata.update_one(
            {"type": "home_update"},
            {"$set": {"timestamp": datetime.datetime.now()}},
            upsert=True
        )

# Function to update the commodity data if necessary
def getCommodities(name, url):
    pass


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/commodities')
def get_all_commodities():
    getHomePage()
    commodities = db.commodities.find()
    return render_template("all_commodities.html", commodities=commodities)


@app.route('/commodity/<name>')
def commodity(name):
    comm_name = db.commodities.find_one({"name": name})
    url = comm_name['url']

    data = db[name].find({})
    return render_template('commodity.html', name=name, data=data)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/search")
def search():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
