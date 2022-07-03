from __future__ import print_function
import urllib.request
import json
import cv2
import threading, time
import requests
from datetime import datetime
import numpy as np
import os
import shutil
import base64
import glob
from ai_func import *

'''
Communication Module : Setting up functions that communicate with the server and functions
that are used by the scheduler (that communicates with ai programs)
'''

# -------------------------------------------------- GET IMAGE
def get_image():
    '''
    # ESP-VERSION
    webserver_path = 'http://192.168.2.120/saved-photo'
    captured_image = 'site_photo.jpg'
    # This line grabs the image from the webserver and saves in CWD as 'site_photo.jpg'
    urllib.request.urlretrieve(webserver_path, captured_image)
    #EOF ESP-VERSION
    '''
    # _________________________________ MOCK VERSION
    mock_url = 'http://127.0.0.1:81'
    urllib.request.urlretrieve(mock_url)
    if len(glob.glob('../../../downloads/pic.jpg')) > 0:
        shutil.move('../../../downloads/pic.jpg', './')
    # __________________________________ EOF MOCK VERSION

# ---------------------------------------------------- ASK FOR NEW MEMBER FROM SERVER
def askforimage():
    print("ask for img (new member)")
    addr = 'http://68.183.201.80:5000'
    ext = '/get_image'
    get_url = addr + ext
    while True:
        time.sleep(10)
        #Make GET reuest to ask for new member (image)
        try:
            response = requests.get(get_url)
        except requests.exceptions.RequestException as e:
            print(f"ERROR: {e}")
            raise SystemExit(e)

        data = response.json() #returns dict containing name and image encoding

        print(data["name"])
        name = data["name"]

        imgFolder = f'images/{name}'
        imgFile = f'images/{name}/{name}.jpg'

        #this error check is here for testing purposes
        #change/remove as real business logic is implemented

        #if this image exists already,
        #then, skip this iteration and wait for NEW member image

        if os.path.exists(imgFile):
            continue

        img_encoded = data["img"]["py/b64"]
        #convert base 64 to byte string (for cv decode method)
        img_encoded = base64.b64decode(img_encoded)

        #convert imgencoded data to byte array,
        #then, decode it into an image
        nparr = np.frombuffer(img_encoded, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        #save new member image to images folder

        if not os.path.exists(imgFolder):
            os.makedirs(imgFolder)
        cv2.imwrite(imgFile, img) #save image to new member folder in images

        #add new member to USERS json
        jsonFile = 'USERS/users.json'
        newObj = []
        if os.path.isfile(jsonFile) is False:
            raise Exception("users.json File NOT found.")

        with open(jsonFile) as fp:
            newObj = json.load(fp)

        newObj.append({
        "first_name": name,
        "image": imgFile,
        })

        with open(jsonFile, 'w') as json_file:
            json.dump(newObj, json_file, indent=4, separators=(',', ': '))

# ------------------------------------------------------------------- PROCESS DETECTION
# keep looking for image TO detect in buffer
def detect():
    while True:
        time.sleep(10)
        get_image()
        pic = glob.glob('pic.jpg') #used to be '*.jpg', change it back later lole
        if len(pic) == 0:
            continue
        print(compare(pic[0])) #now we are detecting and comparing in the exp pic
        os.remove(pic[0])
            #detect is directory where esp has sent an image
#buffer in this case is a folder here that at any point should only have one image in it
#in case the one image buffer not work, do FIFO - check time of image and work on the earlier one
    #ok so there is an image in the folder now
        #call

detect()
