# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory


# face import
from PIL import Image
import face_recognition
import cv2
# face import end

UPLOAD_FOLDER = os.path.dirname(os.path.abspath('static'))+'/static/uploads'
BUILD_FOLDER = os.path.dirname(os.path.abspath('static'))+'/static/build'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BUILD_FOLDER'] = BUILD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)

            img_build_file_path=os.path.join(app.config['BUILD_FOLDER'], filename)
            file.save(img_file_path)
            #return redirect(url_for('uploaded_file',filename=filename))
            img_file=img_file_path
            image = face_recognition.load_image_file(img_file)
            img = cv2.imread(img_file)
            face_locations = face_recognition.face_locations(image)
            print("I found {} face(s) in this photograph.".format(len(face_locations)))
            for face_location in face_locations:
                # Print the location of each face in this image
                top, right, bottom, left = face_location
                print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
                # You can access the actual face itself like this:
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                #pil_image.show() #face图片 单独的
            cv2.imwrite(img_build_file_path,img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
            return render_template('index.html',text=filename)
    if request.method == 'GET':
        return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
