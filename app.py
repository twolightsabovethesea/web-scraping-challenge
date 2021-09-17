from flask import Flask, render_template, redirect

# import pymongo and scrape_mars
# from flask_pymongo import PyMongo

import pymongo

import scrape_mars

from bson.json_util import dumps

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db





# Set route
@app.route('/')
def index():
    
    # Return the template with the mars data passed in
    

    return render_template('index.html', mars=db.mars)
# Set route
@app.route('/scrape')
def scrape():
    # Drops collection if available to remove duplicates
    db.mars.drop()

    post = scrape_mars.scrape()

    db.mars.insert_one(post)


    # Return the template with the teams list passed in
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)
