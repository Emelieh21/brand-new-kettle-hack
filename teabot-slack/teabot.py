import os
import time
from slackclient import SlackClient
import requests
import json

# starterbot's ID as an environment variable
BOT_ID = "<YOUR_BOT_ID>"

# constants
AT_BOT = "<@" + BOT_ID + ">"
MAKE_TEA_COMMAND = "make tea"
STOP_BOILING_COMMAND = "stop boiling"

# instantiate Slack & Twilio clients
slack_client = SlackClient('<YOUR_SLACK_API_TOKEN>')
headers = {'content-type': 'application/json', 'Authorization': '<YOUR_RELAYR_TOKEN>', 'Cache-Control':'no-cache'}


		
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + MAKE_TEA_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(MAKE_TEA_COMMAND):
		data = {'meaning': 'kettle', 'value': 'true'}
		r = requests.post('https://api.relayr.io/devices/<KETTLE_DEVICE_ID>/data', data=json.dumps(data), headers=headers)
		response = "Sure... Your water is boiling now!"
    if command.startswith(STOP_BOILING_COMMAND):
		data = {'meaning': 'kettle', 'value': 'false'}
		r = requests.post('https://api.relayr.io/devices/<KETTLE_DEVICE_ID>/data', data=json.dumps(data), headers=headers)
		response = "OK - I stopped the kettle!"
    if command.startswith("is the kettle boiling?"):
		r = requests.get('https://api.relayr.io/devices/<KETTLE_DEVICE_ID>/readings', headers=headers)
		resp = json.loads(r.text)
		try:
			if resp['readings'][0]['value'] == "true":
				response = "Yes, the kettle is currently boiling."
			if resp['readings'][0]['value'] == "false":
				response = "No, the kettle is currently off."
		except:
			response = "Unfortunately.. I don't know :("
	
	# # Optional: check if the water is hot - only if you have a temperature sensor connected!
	# # uncomment the lines below if you want to add this function
    # if command.startswith("is the water hot?"):
		# r = requests.get('https://api.relayr.io/devices/<KETTLE_TEMPERATURE_DEVICE_ID>/readings', headers=headers)
		# resp = json.loads(r.text)
		# try:
			# if float(resp['readings'][0]['value']) < 25:
				# response = "The water is currently cold. You can say \"make tea\" to me and I will heat it up."
			# if 25 <= float(resp['readings'][0]['value']) <= 45:
				# response = "The water is still quite warm, I can reheat it for you. You can ask me \"make tea\"."
			# if float(resp['readings'][0]['value']) > 45:
				# response = "The water is still hot. Probably it just boiled."
		# except:
			# response = "Unfortunately.. I don't know :("
			
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None
	
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")