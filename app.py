from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'beer_database.db'

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

# Calculate weighted rating for each beer
def calculate_weighted_rating(beer):
    db = get_db()
    cursor = db.cursor()
    style = beer[4]
    cursor.execute("SELECT AVG(rating) FROM beers WHERE style=?", (style,))
    avg_rating = cursor.fetchone()[0]
    if avg_rating:
        weighted_rating = (beer[6] * len(beer)) / (len(beer) + 1) + (avg_rating / (len(beer) + 1))
    else:
        weighted_rating = beer[6]  # No average rating for the style
    return round(weighted_rating, 1)

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
    return redirect(url_for('index'))

@app.route('/delete_beer/<int:id>')
def delete_beer(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM beers WHERE id=?", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
