# YIT-Pybot
RTM enabled slack bot for adding value to YIT Slack. Ran in Docker on Fargate. Coded in Python 3.7.4

# Permissions
You need two types of tokens for this application to work successfully. An admin "workspace" token, which is assigned 
to an individual user, and a bot token assigned to your bot. Certain Slack API methods do not have permissions from a
bot, and therefor a user token is required. 

These two tokens are passed by environment variables as `USER_TOKEN` and `BOT_TOKEN`.

# Debugging
Set the environment variable `DEBUG_ON` to `true` will log debug output for development. 

# Running locally
This can be run on any platform as long as the tokens are passed.
`docker run --rm -d --e BOT_TOKEN='changeme' -e USER_TOKEN='changeme' yamtechnology/yit-pybot:latest`

## Modules
#### messages.py
Contains functions that involve/support sending receiving messages to and from slack. 

#### regex.py
A module that will perform regex lookups on text read from any channel the bot is in. 

#### rtm.py
This executes and runs the bot. 

#### spells.py
Wizardry. See the spells readme for more information.

## Planned features
* Jenkins build stats. Which jobs are failing. Daily/weekly summary. 
* Ticket stats from Jira. How many open and closed per team.
* Database integration to a nosql database for stored state.
* Create `shared-app-channels` with automation. 