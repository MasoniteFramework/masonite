"""Validator Helper Module."""

from ..validator import Validator


def validate(validations, data, messages={}):
    """Helper function for shorthand validations.

    Arguments:
        validations {dict} -- A dictionary of validations from the validator.py library
        data {dict} -- The data to be validated

    Keyword Arguments:
        messages {dict} -- Optional messages to render if there was a bad validation. (default: {{}})

    Returns:
        Bool|dict -- Returns True if validations are good or a dictionary if there are errors.
    """
    validator = Validator().validate(validations)
    validator.error_messages = messages
    if validator.check(data):
        return True
    else:
        return validator.errors()
