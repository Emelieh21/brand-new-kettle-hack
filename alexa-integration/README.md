# Triggering the Kettle to Start Boiling via Alexa

Every time Alexa will be asked "Alexa, ask kettle to start boiling", the lambda function that runs the skill will send an http request with a TRUE value to the relayr cloud. It will be received by the relayr cloud as if it is a device sending out boolean data. 

### Step 1: Create a virtual "device" on the Relayr cloud

First of we need to create a devide on the relayr cloud. Since it is not a real device - we set up a custom model. Login to your relayr developer account, go to the tab "models" on the left side. Click "add new model" and enter the following:

<ADD SCREENSHOTS HERE>

Once this is done, we can create or fake device. Click on add new device and you can click finish right away without changing anything. Give your device a name and now your device should be created.

If you click on the settings wheel in the upper right corner as you see here:

<ADD SCREENSHOT>

You can find the device ID and credentials of your device. We will need these for the next step.



### Step 2: Create an AWS lambda function that makes an HTTP POST request to your virtual relayr "kettle" device

Next step is to make Alexa send a trigger to the kettle each time we want it to start or stop boiling. For this we use [AWS lambda](https://aws.amazon.com/console/) and the [Alexa developer console](developer.amazon.com). For more information on getting started with creating Alexa Skills - see this [tutorial](https://github.com/alexa/skill-sample-nodejs-fact).

**Alexa skill still in progress - lambda_function.py, sample_utterances.txt, intent_schema.json and slot items will be uploaded soon!**

To see a simple example of a HTTP POST request in python to your relayr device, check the [python_http_post_request.py](python_http_post_request.py) file.

The lambda function is in Python. You can upload the lambda_function.py file together with the needed dependencies (in this case this is only the [request](http://docs.python-requests.org/en/master/) module) in a ZIP folder. 

<ADD SCREENSHOTS>

This script makes a http POST request with a "true" value if you tell Alexa _"Ask the kettle to boil/start boiling/start"_ - and a "false" value when you say _"Ask the kettle to stop/abort/stop boiling"_.

The sample utterances, custom slot items and intent_schema.json you can find in this folder soon. 









