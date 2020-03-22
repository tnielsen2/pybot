import requests
import json
import os
from django.http import JsonResponse
# Import my app modules
import messages
import users

## TO DO list:
# Create main function to pull in channel, user and other data by means of decorator payload

# Grammabot.io api key. Grammabot.io has a free, non api key limited to 100 uers per day. Default key should be XYZ
grammarbot_token = os.getenv('GRAMMARBOT_TOKEN')

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
    data = payload['data']
    if 'user' in data:
        # Set some function variables
        web_client = payload['web_client']
        user_id = data['user']
        channel_id = data['channel']
        text = data['text']
        response = requests.post('http://api.grammarbot.io/v2/check', data={
            'api_key': grammarbot_token,
            'language': 'en-US',
            'text': text
        })
        if response.status_code == 200:
            dict = response.json()
            matches = dict['matches']
            if str(matches) != '0':
                messages.send_channel_message('You have {} grammar mistakes in the following text:'.format(str(len(matches))), channel_id)
                messages.send_channel_message('>{}'.format(text), channel_id)
                x = 0
                for error in matches:
                    x = x + 1
                    messages.send_channel_message('********** ERROR NUMBER {} **********'.format(str(x)), channel_id)
                    messages.send_channel_message('Found in the following sentence:', channel_id)
                    messages.send_channel_message('>{}'.format(error['sentence']), channel_id)
                    messages.send_channel_message('Error rule: {}'.format(error['rule']['description']), channel_id)
                    replacements = []
                    if error['shortMessage'] == 'Spelling mistake':
                        for replacement in error['replacements']:
                            replacements.append(replacement['value'])
                        messages.send_channel_message('Suggestion: Learn to spell, or pay careful attention to the red line under what you type. '
                              'Did you mean `{}`?'.format(serialize_list(replacements)), channel_id)
                    else:
                        messages.send_channel_message('Suggestion: {}'.format(error['message']), channel_id)
                    print('')
                x = 0
                return response
        else:
            data = {
                'Error': 'Not 200'
            }
            return JsonResponse(data)
    else:
        return None

# debugging output for testing
#test = check_grammar('How do I Get their? This is SIlY')
# print(json.dumps(test.json(), indent=2))

