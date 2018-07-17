from ..validator import Validator

def validate(validations, data, messages = {}):
    validator = Validator().validate(validations)
    validator.error_messages = messages
    if validator.check(data):
        return True
    else:
        return validator.errors()
        
