from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("getInput.html")

@app.route('/result')
def result():
    return "sdferfer"

if __name__ == '__main__':
    app.run(debug=True)
