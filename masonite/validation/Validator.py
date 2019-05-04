class BaseValidation:

    def __init__(self, validations):
        self.errors = []
        # validations = ['user', 'email']
        self.validations = validations

    def error(self, message):
        self.errors.append(message)

class required(BaseValidation):

    def handle(self, dictionary):
        boolean = True
        for key in self.validations:
            if not key in dictionary:
                boolean = False
                self.error('{} is required'.format(key))

        return boolean


class numeric(BaseValidation):

    def handle(self, dictionary, negation=False):
        boolean = True

        for key in self.validations:
            if key in dictionary and not str(dictionary[key]).isdigit():
                boolean = False
                self.error('{} must be a numeric'.format(key))

        return boolean

    
class string(BaseValidation):

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if key in dictionary and not isinstance(dictionary[key], str):
                boolean = False
                self.error('{} must be a string'.format(key))

        return boolean

class length(BaseValidation):

    def __init__(self, validations, min=1, max=255):
        super().__init__(validations)
        self.min = min
        self.max = max

    def handle(self, dictionary, negation=False):
        boolean = True

        for key in self.validations:
            if key in dictionary and (len(dictionary[key]) < self.min or len(dictionary[key]) > self.max):
                boolean = False
                self.error('{} length must be between {} and {}'.format(key, self.min, self.max))

        return boolean

class json(BaseValidation):

    def handle(self, dictionary):
        import json
        boolean = True
        try:
            for key in self.validations:
                if key in dictionary and not json.loads(dictionary[key]):
                    boolean = False
                    self.error('{} must be json'.format(key))
            
            return boolean
        except (TypeError, json.decoder.JSONDecodeError):
            self.error('{} must be json'.format(key))
            return False


class Validator:

    def __init__(self, dictionary, *rules):
        self.errors = []
        self.validate(dictionary, *rules)

    def validate(self, dictionary, *rules):
        for rule in rules:
            if not rule.handle(dictionary):
                self.errors += rule.errors
