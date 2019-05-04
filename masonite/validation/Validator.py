from masonite.helpers import Dot as DictDot

class BaseValidation:

    def __init__(self, validations, messages={}):
        self.errors = []
        self.messages = messages
        # validations = ['user', 'email']
        self.validations = validations
        self.negated = False

    def error(self, key, message):
        # self.custom_errors = ('you need an email', 'you need a username')
        # self.errors = []
        if key in self.messages:
            self.errors.append(self.messages[key])
            return
        self.errors.append(message)
    
    def find(self, key, dictionary, default=False):
        return DictDot().dot(key, dictionary, default)

    def negate(self):
        self.negated = True
        return self


class required(BaseValidation):

    def handle(self, dictionary):
        boolean = True
        for key in self.validations:
            if not self.find(key, dictionary):
                boolean = False
                self.error(key, '{} is required'.format(key))

        return boolean


class numeric(BaseValidation):

    def handle(self, dictionary, negation=False):
        boolean = True

        for key in self.validations:
            if not str(self.find(key, dictionary)).isdigit():
                boolean = False
                self.error(key, '{} must be a numeric'.format(key))

        return boolean


class string(BaseValidation):

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if key in dictionary and not isinstance(dictionary[key], str):
                boolean = False
                self.error(key, '{} must be a string'.format(key))

        return boolean


class none(BaseValidation):

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if self.find(key, dictionary) is not None:
                boolean = False
                self.error(key, '{} must be None'.format(key))

        return boolean


class length(BaseValidation):

    def __init__(self, validations, min=1, max=255):
        super().__init__(validations)
        if isinstance(min, str) and '..' in min:
            self.min = int(min.split('..')[0])
            self.max = int(min.split('..')[1])
        else:
            self.min = min
            self.max = max

    def handle(self, dictionary, negation=False):
        boolean = True

        for key in self.validations:
            found = self.find(key, dictionary)
            if len(str(found)) < self.min or len(str(found)) > self.max:
                boolean = False
                self.error(key, '{} length must be between {} and {}'.format(key, self.min, self.max))
            elif self.negated:
                self.error(key, '{} length must not be between {} and {}'.format(key, self.min, self.max))
        return boolean


class in_range(BaseValidation):

    def __init__(self, validations, min=1, max=255):
        super().__init__(validations)
        self.min = min
        self.max = max

    def handle(self, dictionary, negation=False):
        boolean = True

        for key in self.validations:
            found = self.find(key, dictionary)
            if found < self.min or found > self.max:
                boolean = False
                self.error(key, '{} must be between {} and {}'.format(key, self.min, self.max))
            elif self.negated:
                print('its negated')
                self.error(key, '{} must not be between {} and {}'.format(key, self.min, self.max))

        return boolean


class equals(BaseValidation):

    def __init__(self, validations, value=''):
        super().__init__(validations)
        self.value = value

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if self.find(key, dictionary) != self.value:
                boolean = False
                self.error(key, '{} must be equal to {}'.format(key, self.value))
            elif self.negated:
                self.error(key, '{} must not be equal to {}'.format(key, self.value))
        return boolean


class greater_than(BaseValidation):

    def __init__(self, validations, value=''):
        super().__init__(validations)
        self.value = value

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if key in dictionary and not dictionary[key] > self.value:
                boolean = False
                self.error(key, '{} must be greater than {}'.format(key, self.value))
            elif self.negated:
                self.error(key, '{} must not be greater than {}'.format(key, self.value))

        return boolean


class less_than(BaseValidation):

    def __init__(self, validations, value=''):
        super().__init__(validations)
        self.value = value

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if key in dictionary and not dictionary[key] < self.value:
                boolean = False
                self.error(key, '{} must be less than {}'.format(key, self.value))
            elif self.negated:
                self.error(key, '{} must not be less than {}'.format(key, self.value))

        return boolean


class isnt(BaseValidation):

    def __init__(self, *rules, value=''):
        super().__init__(rules)
        self.value = value

    def handle(self, dictionary):
        for rule in self.validations:
            if rule.negate().handle(dictionary):
                self.errors += rule.errors


class truthy(BaseValidation):

    def handle(self, dictionary):
        boolean = True

        for key in self.validations:
            if key in dictionary and not dictionary[key]:
                boolean = False
                self.error(key, '{} must be a truthy value'.format(key))

        return boolean


class json(BaseValidation):

    def handle(self, dictionary):
        import json
        boolean = True
        try:
            for key in self.validations:
                if not json.loads(self.find(key, dictionary)):
                    boolean = False
                    self.error(key, '{} must be json'.format(key))

            return boolean
        except (TypeError, json.decoder.JSONDecodeError):
            self.error(key, '{} must be json'.format(key))
            return False


class Validator:

    def __init__(self, dictionary, *rules):
        self.errors = []
        self.validate(dictionary, *rules)

    def validate(self, dictionary, *rules):
        for rule in rules:
            if not rule.handle(dictionary):
                print('rule errors', rule, rule.errors)
                self.errors += rule.errors
