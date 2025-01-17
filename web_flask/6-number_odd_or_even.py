#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """display Hello HBNB!"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def sec_index():
    """display HBNB"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_index(text):
    """C is Fun"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_index(text):
    """Python is Fun"""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def n_index(n):
    """n is a number"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_index(n):
    """n is a number"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """n is a number"""
    if n % 2 == 0:
        even_or_odd = "even"
    else:
        even_or_odd = "odd"
    return render_template('6-number_odd_or_even.html', n=n,
                           even_or_odd=even_or_odd)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
