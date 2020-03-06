import random


meme_council_ids = {
    'bmckendrick': 'U02H26SH1',
    'bshough': 'U5ZTWL0LV',
    'dalgarin': 'UT82EHTLZ',
    'jpobuda': 'U02HXC6U6',
    'lclabaugh': 'UDLV2JQNA',
    'thought': 'URW2FG4RH',
    'tnielsen': 'U6UTB1ZRA'
}

# Return a random user when fed a list of users
def select_random_user(users):
    user, user_id = random.choice(list(users.items()))
    return user_id