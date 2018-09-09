""" Module for miscellaneous helper methods """ 

import random, string

def random_string(length=4):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
