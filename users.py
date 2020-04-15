import random


meme_council_ids = {
    'bmckendrick': 'DERP',
    'bshough': 'DERP',
    'dalgarin': 'DERP',
    'djoyce': 'DERP',
    'jpobuda': 'DERP',
    'lclabaugh': 'DERP',
    'thought': 'DERP',
    'tnielsen': 'DERP'
}

# Return a random user when fed a list of users
def select_random_user(users):
    user, user_id = random.choice(list(users.items()))
    return user_id
