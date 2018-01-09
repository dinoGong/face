# -*- coding: utf-8 -*-
from PIL import Image
import face_recognition
import cv2
# Load the jpg file into a numpy array
img_file="images/1.jpg"
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
cv2.imshow('image',img)
cv2.waitKey(0)
