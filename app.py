from flask import Flask, render_template, jsonify, request

import requests, time, json, pdfminer
import pandas as pd
import collections


app = Flask(__name__)

app.config['FILENAME'] = 'test3'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      return 'file uploaded successfully'

if __name__ == '__main__': app.run(debug=True)