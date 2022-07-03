from __future__ import print_function
import requests
import json
import cv2
from datetime import datetime
import numpy as np
import base64
import urllib.request
from urllib.request import urlretrieve


addr = 'http://68.183.201.80:5000'
ext = '/get_image'
get_url = addr + ext
print("haha wot")
response = requests.get(get_url, headers={'accept': 'application/json'})
#print(response.text)
print("blongbling")
#u = response.decode("utf-8-sig")
data = response.json()
print("ummm")
#OK are we DOING URLLIB AGAIN UMMMMM
#resp_text = urllib.request.urlopen(get_url).read().decode('UTF-8')
# Use loads to decode from text
#data = json.loads(resp_text)
#print(json.loads(response.text))
print(data)
name = data["name"]
img_encoded = data["img"]["py/b64"]
img_encoded = base64.b64decode(img_encoded)


nparr = np.frombuffer(img_encoded, np.uint8)
# decode image
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imwrite("zuko.jpg", img)
