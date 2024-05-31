#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays a HTML page like 8-index.html"""
    states = storage.all("State").values()
    cities = storage.all("City").values()
    amenities = storage.all("Amenity").values()
    places = storage.all("Place").values()
    return render_template('100-hbnb.html', states=states, cities=cities,
                           amenities=amenities, places=places)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

