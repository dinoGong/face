# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import time
from flask import jsonify
import hashlib


# face import
import base64
from PIL import Image
import numpy as np
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

def get_file_md5(file_path):
    md5 = "none"
    if os.path.isfile(file_path):
        f = open(file_path,'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5
def get_img_md5(img):
    md5="none"
    md5_obj = hashlib.md5()
    md5_obj.update(cv2.imencode('.jpg', img)[1])
    hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    print("md5:%s" % (md5))
    return md5
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


def base64_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    imgData = base64.b64decode(encoded_data)
    nparr = np.fromstring(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #img_np = cv2.imdecode(nparr,cv2.CV_LOAD_IMAGE_COLOR)
    return img
def save_img(img):
    millis = int(round(time.time()*1000))

    #filename="%s.png" % (millis)

    img_md5=get_img_md5(img)

    filename="%s.png" % (img_md5)

    img_file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv2.imwrite(img_file_path,img) ##save
    print("\n\n\n path:%s" % (img_file_path))
    return img_file_path

@app.route('/api/face/findfaces',methods=['GET', 'POST'])
def api_findfaces():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        img = base64_to_cv2_img(img_base64)
        img_file_path=save_img(img)


        img_file=img_file_path
        image = face_recognition.load_image_file(img_file)
        #img = cv2.imread(img_file)
        face_locations = face_recognition.face_locations(image)
        faces=len(face_locations)
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
        #cv2.imwrite(img_build_file_path,img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        #cv2.imshow(img)


        #data = cv2.imencode('.jpg', frame)[1].tostring()

        bytes_data = cv2.imencode('.jpg', img)[1]
        content=base64.b64encode(bytes_data)
        #content = base64.encodebytes(bytes_data)
        content=str(content, encoding = "utf-8")
        content="data:image/jpeg;base64,%s" % (content)
        return jsonify(base64=content,faces=faces)

@app.route('/api/face/recognize_faces',methods=['GET', 'POST'])
def api_recognize_faces():
    if request.method == 'POST':

        img_base64_a=request.form['img_base64_a']
        img_base64_b=request.form['img_base64_b']

        img_a = base64_to_cv2_img(img_base64_a)
        img_b = base64_to_cv2_img(img_base64_b)

        img_a_file_path=save_img(img_a)
        img_b_file_path=save_img(img_b)

        image_a = face_recognition.load_image_file(img_a_file_path)
        image_b = face_recognition.load_image_file(img_b_file_path)

        face_a_encoding = face_recognition.face_encodings(image_a)[0]
        face_b_encoding = face_recognition.face_encodings(image_b)[0]

        known_faces = [
            face_a_encoding
        ]

        results = face_recognition.compare_faces(known_faces, face_b_encoding)
        if(results[0]):
            return jsonify(is_same="yes")
        else:
            return jsonify(is_same="no")




@app.route('/')
def home():
    return render_template('index.html',title="face++")
@app.route('/find_faces')
def find_faces():
    return render_template('find_faces.html',title="人脸识别")
@app.route('/recognize_faces')
def recognize_faces():
    return render_template('recognize_faces.html',title="人脸对比")
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
