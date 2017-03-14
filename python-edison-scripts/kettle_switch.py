import mraa
import requests
import json
import time
import datetime

def passed_time(initial_time):
    return datetime.timedelta.total_seconds(datetime.datetime.now() - initial_time) * 1000

flag = False
print(mraa.getVersion())
# Initialize the GPIO 2.
relay = mraa.Gpio(2)
# Set the initialized GPIO as an output.
relay.dir(mraa.DIR_OUT)

headers = {'content-type': 'application/json', 'Authorization': '<Bearer USER_TOKEN>', 'Cache-Control':'no-cache'}

while True:
    r = requests.get('https://api.relayr.io/devices/<DEVICE_ID>/readings', headers=headers)
    response = json.loads(r.text)

    print response['readings'][0]['value']

    if response['readings'][0]['value'] == 'true':
        # Turn on the kettle.
        relay.write(1)
        # Register from what time a "True" value comes in.
        if flag == False:
            last_sent = datetime.datetime.now()
            flag = True
        # If the value has been True for more than a minute (60000 ms), a POST request is send to change to "False."
        if flag == True:
            if passed_time(last_sent) > 60000:
                data = {'meaning': 'kettle', 'value': 'false'}
                r = requests.post('https://api.relayr.io/devices/<DEVICE_ID>/data', data=json.dumps(data), headers=headers)
                flag = False
    else:
        # Turn off the kettle.
        relay.write(0)
        flag = False
    time.sleep(0.5)