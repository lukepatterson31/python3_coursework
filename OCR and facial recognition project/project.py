#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[2]:


import zipfile

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')



def grab_face(img):
    
    cv_img = cv.cvtColor(numpy.array(img), cv.COLOR_RGB2BGR)
    cv_gray_img = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
    #180/185/195
    cv_bin_img = cv.threshold(cv_gray_img, 175, 255, cv.THRESH_BINARY)[1]
    #1.15-1.2 seems best scale
    faces = face_cascade.detectMultiScale(cv_bin_img, scaleFactor=1.15,minNeighbors=4, minSize=(30, 30))
    if len(faces) < 1:
        return 'But there were no faces!'
    face_boxes = faces.tolist()
    
      
    return face_boxes
    
def grab_text(img):
    
    text = pytesseract.image_to_string(img)
    return text


img_dict = {}

with zipfile.ZipFile('readonly/images.zip') as img_zip:
    
    for name, file in zip(img_zip.namelist(), img_zip.infolist()):
        img = img_zip.open(file)
        PIL_img = Image.open(img)
        img_dict[name] = [PIL_img, grab_face(PIL_img), grab_text(PIL_img)]
        print(name)
    
        
   


# In[5]:


face_box_size = 128


for key in img_dict.keys():
    if 'Christopher' in img_dict[key][2]:
        x = 0
        y = 0
        if len(img_dict[key][1]) > 5:
            contact_sheet = Image.new('RGB', (face_box_size * 5, face_box_size * 2))
        else:
            contact_sheet = Image.new('RGB', (face_box_size * 5, face_box_size))
        for face in img_dict[key][1]:
            face_crop = img_dict[key][0].crop((face[0], face[1], face[0] + face[2], face[1] + face[3]))
            face_crop.thumbnail((128, 128))
            contact_sheet.paste(face_crop, (x, y))
            if x < face_box_size * 5:
                x += face_box_size
            else:
                x = 0
                y += face_box_size
        if img_dict[key][1] == "But there were no faces!":
            print('Results found in {}'.format(key))
            print('But there were no faces in that file!')
        else:    
            print('Results found in {}'.format(key))
            display(contact_sheet)
        
        
        


# In[7]:


face_box_size = 128


for key in img_dict.keys():
    if 'Mark' in img_dict[key][2]:
        x = 0
        y = 0
        if len(img_dict[key][1]) > 5:
            contact_sheet = Image.new('RGB', (face_box_size * 5, face_box_size * 2))
        else:
            contact_sheet = Image.new('RGB', (face_box_size * 5, face_box_size))
        for face in img_dict[key][1]:
            face_crop = img_dict[key][0].crop((face[0], face[1], face[0] + face[2], face[1] + face[3]))
            face_crop.thumbnail((128, 128))
            contact_sheet.paste(face_crop, (x, y))
            if x < face_box_size * 5:
                x += face_box_size
            else:
                x = 0
                y += face_box_size
        if img_dict[key][1] == "But there were no faces!":
            print('Results found in {}'.format(key))
            print('But there were no faces in that file!')
        else:    
            print('Results found in {}'.format(key))
            display(contact_sheet)
        
        
        
        


# In[ ]:




