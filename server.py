import phishing_detection
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("getInput.html")

@app.route('/result/<urlname>')
def result(urlname):
    result  = phishing_detection.getResult(urlname)
    return render_template("result.html",result =result)

if __name__ == '__main__':
    app.run(debug=True)
