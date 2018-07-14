from ..validator import Validator

def validate(validations, data):
    validator = Validator().validate(validations)
    if validator.check(data):
        return True
    else:
        return validator.errors()
        
