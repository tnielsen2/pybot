import requests
import json
import os
from django.http import JsonResponse
# Import my app modules
import messages
import users

# Grammabot.io api key. Grammabot.io has a free, non api key limited to 100 users per day.
grammarbot_token = os.getenv('GRAMMARBOT_TOKEN')

# Debugging environment variable.
debug = os.getenv('DEBUG_ON').lower()

# Global variables for spells
grammarck_user = 'none'
grammarck_user_id = 'none'
grammarck_status = False

# Transform a list of strings into a single string to be used in check_grammar
def serialize_list(list):
    z = 0
    str = ''
    z = len(list) - 1
    y = 0
    for word in list:
        y = y + 1
        if y == z:
            str = str + word + ' or '
        elif y == z + 1:
            str = str + word + '?'
        else:
            str = str + word + ' '
    return str

# Feed this function text to get a response from grammarbot if there is a detected error.
# Note: Paid features provide better accuracy, but for someone having problems with their, there and there, this is
# a good choice.
def check_grammar(**payload):
    global grammarck_user
    global grammarck_user_id
    global grammarck_status
    data = payload['data']
    if 'text' in data:
        text = data['text']
    if 'user' in data:
        web_client = payload['web_client']
        channel_id = data['channel']
        user_id = data['user']
        channel_id = data['channel']
        # Allow meme council to disable grammarbot. If disabled, reset the status and users
        if ('!disable grammarbot' in data['text']) and (data['user'] in users.meme_council_ids.values()):
            grammarck_status = False
            if messages.in_channel(grammarck_user, channel_id):
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{grammarck_user}> is no longer being grammar checked."
                )
                grammarck_user = 'none'
            grammarck_user_id = 'none'
        # Allow meme council to enable grammarbot.
        elif ('!enable grammarbot' in data['text']) and (data['user'] in users.meme_council_ids.values()):
            if messages.in_channel(grammarck_user, channel_id):
                grammarck_status = True
                grammarck_user = 'drobertson'
                grammarck_user_id = messages.get_user_id(grammarck_user)
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{grammarck_user}> is now being grammar checked in every channel we share."
                )
        # Mock the user not in the meme council if tyring to enable grammarbot
        elif ('!enable grammarbot' in data['text']) and (data['user'] not in users.meme_council_ids.values()):
            web_client.chat_postMessage(
                channel=channel_id,
                text=f"<@{data['user']}> https://www.youtube.com/watch?v=fBGWtVOKTkM"
            )
        # Mock the user not in the meme council if tyring to disable grammarbot
        elif ('!disable grammarbot' in data['text']) and (data['user'] not in users.meme_council_ids.values()):
            web_client.chat_postMessage(
                channel=channel_id,
                text=f"<@{data['user']}> https://www.youtube.com/watch?v=fBGWtVOKTkM"
            )
        else:
            # Turn on grammarcheck is on and the user is in the channel, then grammar check them.
            if ((grammarck_status is True) and (messages.in_channel(grammarck_user, channel_id))):
                if grammarck_user_id == data['user']:
                    # Set some function variables
                    # Create object from grammarbot api
                    response = requests.post('http://api.grammarbot.io/v2/check', data={
                        'api_key': grammarbot_token,
                        'language': 'en-US',
                        'text': text
                    })
                    if response.status_code == 200:
                        dict = response.json()
                        matches = dict['matches']
                        if debug == 'true':
                            print('DEBUG-Grammarbot-check_grammar: matches variable type:{}'.format(type(matches)))
                            print('DEBUG-Grammarbot-check_grammar: matches variable value:{}'.format(matches))
                        if matches != []:
                            messages.send_channel_message('You have {} grammar mistakes in the following text: `{}`'.format(str(len(matches)), text), channel_id)
                            x = 0
                            for error in matches:
                                x = x + 1
                                quoted_message = '>Error rule: {}'.format(error['rule']['description'])
                                replacements = []
                                if error['shortMessage'] == 'Spelling mistake':
                                    for replacement in error['replacements']:
                                        replacements.append(replacement['value'])
                                    quoted_message = quoted_message + '\n>Suggestion: Learn to spell, or pay careful attention to the red line under what you type.'
                                    quoted_message = quoted_message + '\n>Did you mean `{}`?'.format(serialize_list(replacements))
                                else:
                                    quoted_message = quoted_message + '\n>Suggestion: {}'.format(error['message'])
                                print('')
                                messages.send_channel_message(quoted_message, channel_id)
                                quoted_message = 'ch'
                            x = 0
                            return response
                    else:
                        data = {
                            'Error': 'Not 200'
                        }
                        return JsonResponse(data)
    else:
        return None