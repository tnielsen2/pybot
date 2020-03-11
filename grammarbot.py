import requests
import json
import os
from django.http import JsonResponse

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
def check_grammar(text):
    response = requests.post('http://api.grammarbot.io/v2/check', data={
        'api_key': grammarbot_token,
        'language': 'en-US',
        'text': text
    })
    if response.status_code == 200:
        dict = response.json()
        matches = dict['matches']
        print('You have {} grammar mistakes in the following text:'.format(str(len(matches))))
        print('"{}"'.format((text)))
        x = 0
        for error in matches:
            x = x + 1
            print('ERROR NUMBER {}'.format(str(x)))
            print('Found in the following sentence:')
            print('    "{}"'.format(error['sentence']))
            print('Error rule: {}'.format(error['rule']['description']))
            replacements = []
            if error['shortMessage'] == 'Spelling mistake':
                for replacement in error['replacements']:
                    replacements.append(replacement['value'])
                print('Suggestion: Learn to spell, or pay careful attention to the red line under what you type. '
                      'Did you mean {}?'.format(serialize_list(replacements)))
            else:
                print('Suggestion: {}'.format(error['message']))
            print('')
        x = 0
        return response
    else:
        data = {
            'Error': 'Not 200'
        }
        return JsonResponse(data)

# debugging output for testing
#test = check_grammar('How do I Get their? This is SIlY')
# print(json.dumps(test.json(), indent=2))

