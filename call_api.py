import urllib.request
import json
import base64
import cv2
import numpy as np

# Create dummy image
img = np.zeros((100, 100, 3), dtype=np.uint8)
img[:, :] = (255, 0, 0)
_, buffer = cv2.imencode('.jpg', img)
b64 = base64.b64encode(buffer).decode()
data_url = 'data:image/jpeg;base64,' + b64

data = json.dumps({'name': 'TestUserAPI', 'image': data_url}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/register_face/', data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print('Failed:', e)
