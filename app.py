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
        session.pop('filename_upload',None) 

    return render_template('index.html')

@app.route('/analyse',methods=['GET','POST'])
def analyse():
    if request.method == 'POST' and request.form['flag'] =="index":
        image_file = request.files['image']
        
        #To get the time stamp and store the filename as unique
        timestamp  = time.time()
        
        #save the file in the upload folder 
        image_file_name_list = secure_filename(image_file.filename).split('.')
        filename_img = str(image_file_name_list[0]) + str(timestamp) +"." +str(image_file_name_list[-1])
        session['filename_upload'] = filename_img
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_img))
        compress_ratio  = 60
        
        #compress the image and store in the download folder
        inputpath = app.config['UPLOAD_FOLDER']+session['filename_upload']
        out_filename = filename_img.split('.')[0]+"."+filename_img.split('.')[1]
        outputpath  = app.config['DOWNLOAD_FOLDER'] + out_filename+".jpg"
        methods.compress_image(inputpath,outputpath,quality=int(compress_ratio))
        
        #get the properties of the image
        img_props = methods.image_properties(outputpath)
        full_filename = (os.path.join(app.config['DOWNLOAD_FOLDER'], out_filename+".jpg"))
        
        return render_template('imganalyze.html',image = full_filename , img_props = img_props,compress_ratio = compress_ratio)
    
    
    elif request.method == 'POST' and request.form['flag'] =="analyze":
        compress_ratio = request.form['compressRatio']
        print(compress_ratio)
        img_width = request.form['imgWidth']
        img_height = request.form['imgHeight']
        
        inputpath = app.config['UPLOAD_FOLDER']+session['filename_upload']
        filename_img = session['filename_upload']
        out_filename = filename_img.split('.')[0]+"."+filename_img.split('.')[1]
        outputpath  = app.config['DOWNLOAD_FOLDER'] + out_filename+".jpg"
       
        #to compress the image
        methods.compress_image(inputpath,outputpath,quality=int(compress_ratio))
        #to resize the image
        methods.resize_img(inputpath,outputpath,int(img_width),int(img_height))
        #get the properties of the image
        
        img_props = methods.image_properties(outputpath)
        full_filename = (os.path.join(app.config['DOWNLOAD_FOLDER'], out_filename+".jpg"))
        
        return render_template('imganalyze.html',image = full_filename , img_props = img_props , compress_ratio = compress_ratio)
    
    
    elif request.method == 'GET' :
        print(session['filename_upload'])
        full_filename = (os.path.join(app.config['UPLOAD_FOLDER'], session['filename_upload']))
        return render_template('imganalyze.html',image = full_filename )


# running the server
app.run(debug = True) # to allow for debugging and auto-reload
