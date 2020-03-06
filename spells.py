from random import *
import random
import re
import os
# Import my app modules
import messages
import users

# Slack token is used for admin permissions that are not granted to bot users/apps. This is a "workspace token" from an
# admin user
user_token = os.getenv('USER_TOKEN')

# Bot token is used for reading/writing for an app enabled with "Legacy" bot oath RTM permissions. Current newer
# "granular" permissions do not support RTM.
bot_token = os.getenv('BOT_TOKEN')

# Debugging environment variable.
debug = os.getenv('DEBUG_ON').lower()

# Global variables for spells
silenced_user = 'none'
silenced_user_id = 'none'
silenced_status = False
silenced_timer = 10
silence_roll = 1

# Not a wizard insults
def wizard_insults(user):
    not_a_wizard = ['The only magic <@{}> is capable of is teleporting into work late, and vanishing early.'.format(user),
                    'The only magic <@{}> is capable of is enslaving an entire meeting with meaningless drivel.'.format(user),
                    'The only magic <@{}> is capable of casting is overburden on your team, since they are carrying all the weight.'.format(user),
                    'The only magic <@{}> is capable of casting is poison cloud, with all that microwaved Mountain Dew broccoli.'.format(user),
                    '<@{}> is merely a wand jockey.'.format(user),
                    'A true wizard summons donuts from the nether regions.',
                    'A true wizard has more stickers on their desk than you, at all times.']
    insult = random.choice(not_a_wizard)
    return insult


def silence(**payload):
    global silenced_status
    global silenced_timer
    global silenced_user
    global silenced_user_id
    global silence_roll
    data = payload['data']
    if 'user' in data:
        # Set some function variables
        web_client = payload['web_client']
        channel_id = data['channel']
        #channel_members = messages.get_channel_members(channel_id)
        # Debug printing
        if debug == 'true':
            print('DEBUG: silenced_user={}'.format(silenced_user))
            print('DEBUG: silenced_user_id={}'.format(silenced_user_id))
            print('DEBUG: silenced_status={}'.format(silenced_status))
            print('DEBUG: silenced_timer={}'.format(silenced_timer))
        # Check to see if they are trying to throw a save
        if re.search('^!(R|r)(O|o)(L|l)(L|l)', data['text']):
            if debug == 'true':
                print('DEBUG: !roll regex detected')
                print('DEBUG: data text={}'.format(data['text']))
                print('DEBUG: data user_id={}'.format(data['user']))
            if (data['user'] == silenced_user_id) and (silenced_status is True):
                silence_roll = randint(1, 20)
                # Debug printing
                if debug == 'true':
                    print('DEBUG: Silence roll={}'.format(silence_roll))
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{silenced_user}> has rolled a {str(silence_roll)}!"
                )
                if silence_roll == 20:
                    silenced_status = False
                    silenced_timer = 30
                    web_client.chat_postMessage(
                        channel=channel_id,
                        text=f"<@{silenced_user}> had luck on their side, the spell is no longer effective!!"
                    )
        # Allow meme council to dispel the current spell
        if ('!dispel silence' in data['text']) and (data['user'] in users.meme_council_ids.values()):
            silenced_status = False
            silenced_timer = 30
            web_client.chat_postMessage(
                channel=channel_id,
                text=f"<@{silenced_user}> has had their silence spell dispelled by <@{data['user']}>."
            )
        if silenced_status == True:
            silenced_timer = silenced_timer - 1
            # Dispel silence if timer hits 0
            if silenced_timer == 0:
                silenced_status = False
                silenced_timer = 30
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{silenced_user}> is no longer silenced."
                )
            if data['user'] == silenced_user_id:
                messages.delete_channel_message(data['ts'], data['channel'])
        # Cast silence, if you are a member of the meme council
        elif re.search('^!(S|s)(I|i)(L|l)(E|e)(N|n)(C|c)(E|e)', data['text']):
            if data['user'] in users.meme_council_ids.values():
                # Silence spell global variables
                silenced_user = data['text'].split()[1]
                silenced_user_id = messages.get_user_id(silenced_user)
                if messages.in_channel(silenced_user, channel_id) == True:
                    silenced_status = True
                    web_client.chat_postMessage(
                        channel=channel_id,
                        text=f"<@{silenced_user}> has been silenced! <@{silenced_user}> must pass a saving throw of 20 to break the spell early. `!roll` to save."
                    )
                else:
                    web_client.chat_postMessage(
                        channel=channel_id,
                        text=f"<{silenced_user}> does not exist or is not in this channel."
                    )
            elif data['user'] not in users.meme_council_ids.values():
                web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"<@{data['user']}> is not a wizard. {wizard_insults(data['user'])}"
                )
            else:
                return None

    else:
        return None