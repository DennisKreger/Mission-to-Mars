from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    print(mars)
    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_all():
    mars= mongo.db.mars

    # Run the scrape function
    mars_data = scraping.scrape_all()

    # Update the Mongo database using update and upsert=True
    mars.replace_one({}, mars_data, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug= True)
    app.run()