from __future__ import print_function
import requests
import json
import cv2
from datetime import datetime
import numpy as np
import base64
#import urllib.request
from urllib.request import urlretrieve


addr = 'http://127.0.0.1:5000'
ext = '/get_image'
get_url = addr + ext

response = requests.get(get_url)
data = response.json()
#print(json.loads(response.text))
print(data)
name = data["name"]
img_encoded = data["img"]["py/b64"]
img_encoded = base64.b64decode(img_encoded)


nparr = np.frombuffer(img_encoded, np.uint8)
# decode image
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imwrite("purple.jpg", img)
