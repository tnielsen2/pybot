import os
import slack
import sys

# Slack token is used for admin permissions that are not granted to bot users/apps. This is a "workspace token" from an
# admin user
user_token = os.getenv('USER_TOKEN')

# Bot token is used for reading/writing for an app enabled with "Legacy" bot oath RTM permissions. Current newer
# "granular" permissions do not support RTM.
bot_token = os.getenv('BOT_TOKEN')

# Debugging environment variable.
debug = os.getenv('DEBUG_ON').lower()

### Delete a message from a channel
# ts = Timestamp of message. '1583460770.003100'
# channel_id = Channel id. Ex: 'CKQDUH7M2'
def delete_channel_message(ts, channel_id):
    client = slack.WebClient(token=user_token)
    client.chat_delete(
        token=user_token,
        channel=channel_id,
        ts=ts
    )

### Send a message to a channel as the bot
# message = The message you want to send. Ex: 'Eat it cooter'
# channel_id = Channel id. Ex: 'CKQDUH7M2'
def send_channel_message(message, channel_id):
    client = slack.WebClient(token=bot_token)
    client.chat_postMessage(
      channel=channel_id,
      text=message,
    )

### Get channel information
def get_channel_info(channel_id):
    client = slack.WebClient(token=bot_token)
    channel_info = client.channels_info(
        channel=channel_id,
    )
    return channel_info

### Get channel members
def get_channel_members(channel_id):
    member_list = []
    client = slack.WebClient(token=bot_token)
    groups_list = client.groups_list(
    )
    # Loop through groups first, if its a private channel, we can get the members of it with this method.
    for group in groups_list['groups']:
        if channel_id == group['id']:
            member_list = group['members']
    # If there are no groups, try the channel_info method instead
    if member_list == []:
        channel_info = client.channels_info(
            channel=channel_id
        )
        member_list = channel_info['channel']['members']
    return member_list



### Get workspace members
def get_workspace_members():
    client = slack.WebClient(token=bot_token)
    workspace_users = client.users_list(
        token=bot_token,
    )
    return workspace_users['members']

### Get user id
def get_user_id(username):
    # Retrieve all workspace members for comparison
    workspace_members = get_workspace_members()
    # Loop through workspace members to get the users user_id
    for user in workspace_members:
        # If found, loop through channel members
        if username == user['name']:
            user_id = user['id']
            if debug == 'true':
                print('DEBUG: Module: Messages:')
                print('       Function: get_user_id')
                print('       user_id={}'.format(user_id))
            return user_id

### In channel
# Will return boolean value indicating if the user is in the channel or not based on username (not userid)
# Only works for public channels
def in_channel(username, channel_id):
    # Retrieve all workspace members for comparison
    workspace_members = get_workspace_members()
    # Loop through workspace members to get the users user_id
    for user in workspace_members:
        # If found, loop through channel members
        if username == user['name']:
            user_id = user['id']
            if user_id in get_channel_members(channel_id):
                return True
            else:
                return False
