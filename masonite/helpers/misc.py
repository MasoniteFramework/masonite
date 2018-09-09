""" Module for miscellaneous helper methods """

import random
import string


def random_string(length=4):
    """Generates a random string based on the length given
    
    Keyword Arguments:
        length {int} -- The amount of the characters to generate (default: {4})
    
    Returns:
        string
    """
    
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )
