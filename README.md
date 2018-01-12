# face

#arch linux

首先，更改pip为国内源：

```
nano $HOME/.pip/pip.conf
```

```
[global]
index-url = http://pypi.douban.com/simple
```

安装必要的工具：

```
# pacman -S cmake
# pacman -S boost
# pacman -S opencv
# pacman -S hdf5
```
安装dlib：

```
# wget http://dlib.net/files/dlib-19.8.tar.bz2
# tar jxvf dlib-19.8.tar.bz2
# cd dlib-19.8
# python setup.py install
```

或者

```
sudo pip install dlib
```

安装pip，如果没有的话：
```
# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
```
接下来安装python包：
```
# pip install pillow
# pip install numpy
# pip install opencv-python
# install boost
# install Flask
# install pillow
# install face_recognition
```

运行：
```
python main.py
```

查看效果：
```
http://localhost:5000
```


###freebsd
```
# pkg install cmake
# pkg install wget
# wget http://dlib.net/files/dlib-19.8.tar.bz2
# tar jxvf dlib-19.8.tar.bz2
# python setup.py install
```
如果安装不成功，也可以：

```
# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
```
```
pip install boost
```
```
# pkg install gcc
# pkg install python36
# pkg install py36-pillow
```

```
@app.route('/upload', methods=['GET', 'POST'])
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
        return render_template('face.html',title="面部识别")
```



###debian
安装必要的编译工具
```
apt install cmake build-essential libgtk-3-dev
apt install libboost-all-dev
```

# wget https://bootstrap.pypa.io/get-pip.py
# python get-pip.py

如果用的是云服务器（虚拟机），增加交换内存。
```
dd if=/dev/zero of=/swap bs=1024 count=1M
mkswap /swap
swapon /swap
echo "/swap  swap  swap  sw  0  0" >> /etc/fstab
```
下载并安装dlib
```
wget http://dlib.net/files/dlib-19.8.tar.bz2
tar jxvf dlib-19.8.tar.bz2
cd dlib-19.8
python setup.py
```
设置成pip国内五道口职业技术学院的源

```
# mkdir $HOME/.pip
# nano $HOME/.pip/pip.conf
```
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
[install]
trusted-host=pypi.tuna.tsinghua.edu.cn   
```

然后一路安装python包
```
pip install Flask
pip install pillow
pip install numpy
pip install face_recognition
```




#armbian && dietpi


在nanopi、orangepi和树梅派上面安装。
