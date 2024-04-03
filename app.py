from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database connection
conn = sqlite3.connect('beer_database.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS beers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             brewery TEXT NOT NULL,
             abv REAL NOT NULL,
             style TEXT NOT NULL,
             ibu INTEGER NOT NULL,
             rating REAL NOT NULL)''')
conn.commit()

# Route to render the homepage
@app.route('/')
def index():
    # Fetch all beers from the database
    c.execute('SELECT * FROM beers')
    beers = c.fetchall()
    return render_template('index.html', beers=beers)

# Route to handle adding a new beer
@app.route('/add_beer', methods=['POST'])
def add_beer():
    name = request.form['name']
    brewery = request.form['brewery']
    abv = request.form['abv']
    style = request.form['style']
    ibu = request.form['ibu']
    rating = request.form['rating']
    
    # Insert the new beer into the database
    c.execute("INSERT INTO beers (name, brewery, abv, style, ibu, rating) VALUES (?, ?, ?, ?, ?, ?)",
              (name, brewery, abv, style, ibu, rating))
    conn.commit()
    
    # Redirect back to the homepage after adding the beer
    return redirect(url_for('index'))

# Route to handle deleting a beer
@app.route('/delete_beer/<int:id>')
def delete_beer(id):
    # Delete the specified beer from the database
    c.execute("DELETE FROM beers WHERE id=?", (id,))
    conn.commit()
    
    # Redirect back to the homepage after deleting the beer
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

