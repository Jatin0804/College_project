import datetime
from flask import Flask,  render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from pymongo import MongoClient

# install database packages
from database.createDB_home import createHomeDB
from database.createDB_commodity import createComDB
from database.clean_homepage import createHomeDB_clean

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

client = MongoClient('mongodb+srv://tryuser:123123123@scraper.bsq1upl.mongodb.net/?retryWrites=true&w=majority&appName=scraper')
db = client.commodityDB
db.metadata.drop()

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


# Function to update the home page data if necessary
def getHomePage_clean():
    last_update = db.metadata.find_one({"type": "home_update_clean"})
    if not last_update or (datetime.datetime.now() - last_update['timestamp']).total_seconds() > 86400:
        createHomeDB_clean()
        db.metadata.update_one(
            {"type": "home_update_clean"},
            {"$set": {"timestamp": datetime.datetime.now()}},
            upsert=True
        )

# Function to update the commodity data if necessary
def getCommodities(name, url):
    last_update = db.metadata.find_one({"type": "commodity_update", "name": name})
    if not last_update or (datetime.datetime.now() - last_update['timestamp']).total_seconds() > 86400:
        createComDB(name, url)
        db.metadata.update_one(
            {"type": "commodity_update", "name": name},
            {"$set": {"timestamp": datetime.datetime.now()}},
            upsert=True
        )


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/commodities')
def get_all_commodities(vis=False):
    getHomePage()
    commodities = db.commodities.find()
    if vis:
        return redirect(url_for("get_all_commodities_clean"))
    return render_template("all_commodities.html", commodities=commodities)


@app.route('/commodities/clean')
def get_all_commodities_clean():
    getHomePage_clean()
    commodities = db.clean_commodities.find()
    return render_template("all_commodities.html", commodities=commodities, vis=True)


@app.route('/commodity/<name>')
def commodity(name):
    comm_name = db.commodities.find_one({
        "C_Name": name
    })
    url = comm_name.get('URL')
    getCommodities(name, url)
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
