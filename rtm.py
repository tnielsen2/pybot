import os
import json
from slack import RTMClient
# Import my own modules
import regex
import spells
import grammarbot

# Slack token is used for admin permissions that are not granted to bot users/apps. This is a "workspace token" from an
# admin user
user_token = os.getenv('USER_TOKEN')

# Bot token is used for reading/writing for an app enabled with "Legacy" bot oath RTM permissions. Current newer
# "granular" permissions do not support RTM.
bot_token = os.getenv('BOT_TOKEN')

# Debugging environment variable.
debug = os.getenv('DEBUG_ON').lower()

@RTMClient.run_on(event="message")
def pybot(**payload):
  # Declare global variables here
  data = payload['data']
  # Print payload when debugging
  if debug == 'true':
    print(json.dumps(data, indent=4, sort_keys=True))
  # Regex functions
  regex.dmd(**payload)
  # Spell Functions
  spells.silence(**payload)
  # Grammarbot
  grammarbot.check_grammar(**payload)

rtm_client = RTMClient(token=bot_token)
rtm_client.start()