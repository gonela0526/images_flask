# app.py
from fileinput import filename
from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
import methods
import os
import time



app = Flask(__name__,static_url_path="/static") # name for the Flask app (refer to output)
app.secret_key = 'seceret_img_key'

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['DOWNLOAD_FOLDER'] = 'static/downloads/' 

@app.route('/',methods=['GET'])
def home():
    return '<h1>Image Compress</h1>'


@app.route('/upload',methods=['GET','POST'])
def upload():
    if 'filename_upload' in session:
        session.pop('username',None) 

    return render_template('index.html')

@app.route('/analyse',methods=['GET','POST'])
def analyse():
    if request.method == 'POST':
        image_file = request.files['image']
        timestamp  = time.time()
        image_file_name_list = secure_filename(image_file.filename).split('.')
        filename_img = str(image_file_name_list[0]) + str(timestamp) +"." +str(image_file_name_list[-1])
        session['filename_upload'] = filename_img
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_img))
        full_filename = (os.path.join(app.config['UPLOAD_FOLDER'], filename_img))
    return render_template('imganalyze.html',image = full_filename)    



@app.route('/download', methods=['GET','POST'])
def download():
    if request.method == 'POST':
        compress_ratio = request.form['compresRatio']
        inputpath = app.config['UPLOAD_FOLDER']+session['filename_upload']
        print(inputpath)
        print(compress_ratio)
        filename_img = session['filename_upload']
        out_filename = filename_img.split('.')[0]+"."+filename_img.split('.')[1]
        outputpath  = app.config['DOWNLOAD_FOLDER'] + out_filename+".jpg"
        methods.compress_image(inputpath,outputpath,quality=int(compress_ratio))
        out_full_filename = (os.path.join(app.config['DOWNLOAD_FOLDER'],out_filename+".jpg"))
        return render_template('downloadimage.html',image = out_full_filename)

# running the server
app.run(debug = True) # to allow for debugging and auto-reload
