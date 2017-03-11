import requests
import json

headers = {'content-type': 'application/json', 'Authorization': '<YOUR_TOKEN_HERE', 'Cache-Control':'no-cache'}
data = {'meaning': 'kettle', 'value': 'true'}

r = requests.post('https://api.relayr.io/devices/<YOUR_DEVICE_ID_HERE>/data', data=json.dumps(data), headers=headers)
print r.text
