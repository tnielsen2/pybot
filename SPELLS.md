## Spells

#### Silence

Silence a user for an short period of time. Delete a user's post in every channel that is shared with pybot.

After 30 messages are received (from any user in any channel), then remove silence from the user. Instead of this being
time based, it counts down by a timer.

**Usage:**
`!silence username`

The spell can be broken early by a user issuing the `!roll` command. If they roll a 20, they will break the spell 
"early".

Members of the meme-council can dispel silence by issuing the `!dispel silence` command in any channel shared with
pybot. 