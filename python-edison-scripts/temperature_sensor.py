
import math
import mraa
import requests
import json
import time
import datetime

# More info here -> http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor

B=3975
ain = mraa.Aio(1)

headers = {'content-type': 'application/json', 'Authorization': 'Bearer <USER_TOKEN>', 'Cache-Control':'no-cache'}

while True:
    a = ain.read()
    resistance = (1023-a)*10000.0/a
    temp = 1/(math.log(resistance/10000.0)/B+1/298.15)-273.15
    num = str(round(temp,2))
    data = {'meaning': 'temperature', 'value': num}
    r = requests.post('https://api.relayr.io/devices/<DEVICE_ID>/data', data=json.dumps(data), headers=headers)

    print data
    time.sleep(2)
