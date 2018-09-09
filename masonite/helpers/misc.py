""" Module for miscellaneous helper methods """ 

import random, string

def random_string(length=4):
    rnd_string = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
    return rnd_string
