# YIT-Pybot
RTM enabled slack bot for adding value to YIT Slack. Ran in Docker on Fargate. 

### Planned features

* Jenkins build stats. Which jobs are failing. Daily/weekly summary. 
* Ticket stats from Jira. How many open and closed per team.
* Database integration to a nosql database for stored state 

## Modules
#### messages.py
Contains functions that involve/support sending receiving messages to and from slack. 

#### regex.py
A module that will perform regex lookups on text read from any channel the bot is in. 

#### rtm.py
This executes and runs the bot. 

#### spells.py
Wizardry. See the spells readme for more information. 