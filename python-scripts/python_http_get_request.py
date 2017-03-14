import requests
import json

headers = {'content-type': 'application/json', 'Authorization': '<YOUR TOKEN HERE>', 'Cache-Control':'no-cache'}

r = requests.get('https://api.relayr.io/devices/<YOUR DEVICE ID HERE>/readings', headers=headers)
response = json.loads(r.text)
print type(response['readings'][0]['value'])