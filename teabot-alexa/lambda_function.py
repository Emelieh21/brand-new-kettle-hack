import requests
import json

def lambda_handler(event, context):
    if (event['session']['application']['applicationId'] != "<OPTIONAL:YOUR_ALEXA_APP_ID_HERE>"):
        #raise ValueError("Invalid Application ID")
        pass
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
		
def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "KettleIntent":
        return start_kettle(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    return handle_session_end_request()
    print "Ending session."
    # Cleanup goes here...

def get_welcome_response():
    session_attributes = {}
    card_title = "Kettle"
    speech_output = "Hallo! What would you like your kettle to do?"
    reprompt_text = "What do you want your kettle to do?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Kettle"
    speech_output = "Bye bye!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def start_kettle(intent):
    session_attributes = {}
    card_title = "Kettle"
    speech_output = "Something went wrong here. Oops."
    reprompt_text = "I am not sure what you want me to tell your Kettle to do for you."
    should_end_session = True
    
    try:
        itemOne = str(intent['slots']['itemOne']['value'])
        headers = {'content-type': 'application/json', 'Authorization': '<YOUR_RELARY_TOKEN_HERE>', 'Cache-Control':'no-cache'}

        if itemOne in ("boil", "to boil", "start", "make me a tea", "start boiling"):
            data = {'meaning': 'kettle', 'value': 'true'}
            r = requests.post('https://api.relayr.io/devices/<YOUR_RELAYR_DEVICE_ID_HERE>/data', data=json.dumps(data), headers=headers)
            resp = "Maybe your kettle will start"
            try:
                html = str(r)
                html = html.replace(">", "")
                html = html.replace("<", "")
                if html == "Response [202]":
                    resp = "Your kettle will boil."
                else:
                    resp = "Sorry. Your kettle won't boil."
            except:
                pass
            
        elif itemOne in ("stop", "to stop", "stop boiling", "abort"):
            data = {'meaning': 'kettle', 'value': 'false'}
            r = requests.post('https://api.relayr.io/devices/<YOUR_RELAYR_DEVICE_ID_HERE>/data', data=json.dumps(data), headers=headers)
            resp = "Maybe your kettle will stop"
            try:
                html = str(r)
                html = html.replace(">", "")
                html = html.replace("<", "")
                if html == "Response [202]":
                    resp = "Your kettle will stop."
                else:
                    resp = "Sorry. Your kettle won't stop."
            except:
                pass
    except:
        resp = "Oops. I did not quite get that. Please try again."
        should_end_session = False
        
    speech_output = resp
		 

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
			