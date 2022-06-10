from __future__ import print_function
import requests
import json
import cv2
from datetime import datetime
#import urllib.request
from urllib.request import urlretrieve


addr = 'http://68.183.201.80:5000'
ext = '/get_image'
get_url = addr + ext

currtime = datetime.now()
imgname = currtime.strftime("%H%M%S.jpg")

urlretrieve(get_url, imgname)
#prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}
'''
requests.get(get_url, stream=True)

#print(r.text())

response = requests.post(get_url, headers=headers)
r = response #json.loads(response.text)
print(f"RESPONSE IS  {r}  u got itttt?\n\n")


currtime = datetime.now()
imgname = currtime.strftime("%H%M%S")

#img_json = json.loads(r.text)
img = cv2.imdecode(r, cv2.IMREAD_COLOR)
cv2.imwrite(imgname, img)

# decode response
print(r.text)
'''
