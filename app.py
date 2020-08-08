from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, send_file
from flask import send_from_directory

import requests, time, json, pdfminer
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import collections
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['XML_FOLDER'] = 'xml_files'
app.config['CSV_FOLDER'] = 'csv_files'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def page_to_csv(purifieddict, category, region, usagetype, defaultxpos):
	print(category, region, usagetype)
	csv_appender = []
	# print(defaultxpos)
	for key in purifieddict:
		lin = sorted(purifieddict[key], key=lambda x: float(x[2]))
	if len(lin)==2:
	  if float(lin[0][2])==defaultxpos[0]:
	    category = lin[0][0]
	  elif float(lin[0][2])==defaultxpos[1]:
	    region = lin[0][0]
	  elif float(lin[0][2])==defaultxpos[2]:
	    usagetype = lin[0][0]
	elif len(lin)==3:
	  # print(category, region, usagetype)
	  # print(' '.join([x[0] for x in purifieddict[key]]))
	  if category and region and usagetype:
	    csv_appender.append([category, region, usagetype]+[x[0] for x in sorted(purifieddict[key], key=lambda x: float(x[2]))])
	print(category, region, usagetype)
	return [csv_appender, category, region, usagetype]

def process_pdf(filename):
	filename = filename.replace('.pdf', '')
	xml_file_path = os.path.join(app.config['XML_FOLDER'], filename+'.xml')
	pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.pdf')
	csv_file_path = os.path.join(app.config['CSV_FOLDER'], filename+'.csv')
	os.system('pdf2txt.py -o {} {}'.format(xml_file_path, pdf_file_path))
	soup = BeautifulSoup(open('{}'.format(xml_file_path)).read())
	defaultxpos = ['76.074', '85.272', '86.191']
	master_csv = []
	pageno = 0
	category = ''
	region = ''
	usagetype = ''
	xset = set()
	xlist = []
	list_mastersamples = []


	for page in soup.find_all('page'):
	  pageno+=1
	  mastersample = collections.defaultdict(list)
	  for box in page.find_all('textbox'):
	    tmp = []
	    for line in box.find_all('textline'):
	      y_val = line.find('text')['bbox'].split(',')[1]
	      x_val = line.find('text')['bbox'].split(',')[0]
	      size = line.find('text')['size']
	      value = ''.join([i.text for i in line.find_all('text')])
	      if value.encode('utf-8')!='' and value.encode('utf-8')!='\xc2\xa0\n' and 'Page' not in value:
	        tmp.append([value.encode('utf-8').decode('utf-8','ignore').replace(u'\xa0', u' ').replace(u'\xb7', u'').strip(), y_val, x_val, size])
	    if tmp:
	      for t in tmp:
	        sent, y, x, size = t
	        mastersample[float(y)].append([sent, y, x, size])
	        if float(x)<100:
	          xset.add(float(x))
	          xlist.append(float(x))
	  list_mastersamples.append(mastersample)

	defaultxpos = [x[0] for x in collections.Counter(xlist).most_common(3)][::-1]
	for mastersample in list_mastersamples:
	  result, category, region, usagetype = page_to_csv(mastersample, category, region, usagetype, defaultxpos)
	  master_csv+=result

	df = pd.DataFrame(master_csv, columns=['Category', 'Region', 'Usagetype', 'Description', 'Quantity', 'Cost'])
	df.to_csv('{}'.format(csv_file_path), index=None)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_pdf(filename)
            print(os.listdir('uploads'))
            print(os.listdir('xml_files'))
            print(os.listdir('csv_files'))
            return send_file(os.path.join(app.config['CSV_FOLDER'], filename.replace('.pdf', '')+'.csv'))
            # return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__': app.run(debug=True)