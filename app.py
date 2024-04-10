from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import requests

app = Flask(__name__)

DATABASE = 'beer_database.db'

# Unsplash API access key
ACCESS_KEY = 's0R8jX06y2cKi-ZNxLcdXhyPthQKvCCxrcwY14Hfs1Y'
# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



def search_image(query):
    # Make an HTTP GET request to search for images related to the query
    url = f'https://api.unsplash.com/search/photos?query={query}&client_id={ACCESS_KEY}'
    response = requests.get(url)
    data = response.json()
    # Extract the URL of the first image from the API response
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['urls']['regular']
    else:
        return None


# Calculate weighted rating for each beer
def calculate_weighted_rating(beer):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT AVG(rating) FROM beers WHERE style=?", (beer[4],))
    avg_rating = cursor.fetchone()[0]
    return round(avg_rating, 1)


# Routes
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM beers')
    beers = cursor.fetchall()

    # Calculate weighted rating for each beer
    beers_with_weighted_rating = []
    for beer in beers:
        weighted_rating = calculate_weighted_rating(beer)
        beers_with_weighted_rating.append((*beer, weighted_rating))

    return render_template('index.html', beers=beers_with_weighted_rating)

@app.route('/add_beer', methods=['POST'])
def add_beer():
    db = get_db()
    cursor = db.cursor()
    name = request.form['name']
    brewery = request.form['brewery']
    abv = request.form['abv']
    style = request.form['style']
    ibu = request.form['ibu']
    rating = request.form['rating']
    cursor.execute("INSERT INTO beers (name, brewery, abv, style, ibu, rating) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, brewery, abv, style, ibu, rating))
    db.commit()
    update_all_beer_ratings()
    # Search for images related to the beer's name using the Unsplash API
    image_url = search_image(name)

    # Pass the image URL along with other form data to the template
    return render_template('beer_added.html', name=name, brewery=brewery, image_url=image_url)
    

@app.route('/delete_beer/<int:id>')
def delete_beer(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM beers WHERE id=?", (id,))
    db.commit()
    return redirect(url_for('index'))

def update_all_beer_ratings():
    db = get_db()
    cursor = db.cursor()
    
    # Get all beers from the database
    cursor.execute("SELECT * FROM beers")
    all_beers = cursor.fetchall()
    
    # Iterate through each beer and update its rating
    for beer in all_beers:
        beer_id = beer[0]
        new_rating = calculate_weighted_rating(beer)
        
        # Update the beer's rating in the database
        cursor.execute("UPDATE beers SET rating=? WHERE id=?", (new_rating, beer_id))
    
    # Commit the changes to the database
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(debug=True)
