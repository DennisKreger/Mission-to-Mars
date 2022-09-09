# Import Dependencies 
from flask import Flask, render_template, redirect, url_for 
from flask_pymongo import PyMongo
import scrape_mars



# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
#app.config["MONGO_URI"] = os.environ.get('authentication')
#mongo = PyMongo(app)



# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index(): 

    # Find data
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    #mars_data = scrape_mars.scrape_mars_image()
    #mars_data = scrape_mars.scrape_mars_facts()
    #mars_data = scrape_mars.scrape_mars_weather()
    #mars_data = scrape_mars.scrape_mars_hemispheres()
    mars.update({}, {"$set":mars_data}, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)