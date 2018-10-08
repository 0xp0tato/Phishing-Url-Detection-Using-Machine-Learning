import os
import phishing_detection
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER= '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result')
def result():
    urlname  = request.args['name']
    result  = phishing_detection.getResult(urlname)
    return result

# @app.route('/upload')
# def upload():
# 	return 'yes'

@app.route('/', methods = ['GET', 'POST'])
def hello():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('no file part')
			return "false"
		file = request.files['file']
		if file.filename == '':
			flash('no select file')
			return 'false'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			contents = file.read()
			with open("files/URL.txt","wb") as f:
				f.write(contents)
			file.save = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return render_template("getInput.html")
	return  render_template("getInput.html")

			











if __name__ == '__main__':
    app.run(debug=True)
