from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of a Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record
    mars_data = mongo.db.mars_data.find_one()
    
    # Return data and template
    return render_template("index.html", mars_data=mars_data)
    
# Route the scrape funtion trigger
@app.route("/scrape")
def scrape_all():
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", 302)

if __name__ == "__main__":
    app.run(debug=True)
    