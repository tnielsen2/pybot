import re
from random import *
import random

dmd_list = [
    'Dangerously mad Daryl',
    'Darren messaged Daryl',
    'Dent master Daryl',
    'Dead monitor Daryl',
    'Delaware mudflap Daryl',
    'Diablo mobile Daryl',
    'Dial-up modem Daryl',
    'Diabetes master Daryl',
    'Dickbutt master Daryl',
    'Don\'t manage Daryl',
    'Don\'t mention Daryl',
    'Don\'t mentor Daryl',
    'Downtime maker Daryl',
    'Downtime maintenance Daryl',
    'Drunken mess Daryl',
    'Driving master Daryl',
    'Dual motor Daryl',
    'Dual man-bun Daryl',
    'Duo mobile Daryl',
    'Dump master Daryl',
    'Dunce mage Daryl',
    'Dumpster manager Daryl',
    'Dutch master Daryl',
    'Dutch mom Daryl'
]

daryl_misspellings = ['D\'rell',
                      'D`ray L',
                      'Darule',
                      'Darylen'
                      'Daryle',
                      'Darrel',
                      'Darlin',
                      'Darlene',
                      'Darylene',
                      'Daryl',
                      'D\'darlhen']

# If daryl is found in the string of a users message
def dmd(**payload):
    data = payload['data']
    web_client = payload['web_client']
    if 'user' in data:
        if re.search('(D|d)(a|A)(r|R)(y|Y)(l|L)', data['text']):
            chance = 0
            chance = randint(1, 20)
            if chance == 1:
                dmd_phrase = random.choice(dmd_list)
                daryl_misspelled_name = random.choice(daryl_misspellings)
                channel_id = data['channel']
                user = data['user']
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{user}> should know better. {daryl_misspelled_name} prefers to be referred to as \"{dmd_phrase}\"!"
                )