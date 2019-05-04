from masonite.helpers import Dot as DictDot


class BaseValidation:

    def __init__(self, validations, messages={}):
        self.errors = []
        self.messages = messages
        self.validations = validations
        self.negated = False

    def passes(self, attribute, key, dictionary):
        return True

    def error(self, key, message):
        if key in self.messages:
            self.errors.append(self.messages[key])
            return
        self.errors.append(message)

    def find(self, key, dictionary, default=False):
        return DictDot().dot(key, dictionary, default)

    def message(self, key):
        return ''

    def negate(self):
        self.negated = True
        return self

    def handle(self, dictionary):
        boolean = True
        for key in self.validations:
            if self.negated:
                if self.passes(self.find(key, dictionary), key, dictionary):
                    boolean = False
                    if hasattr(self, 'negated_message'):
                        self.error(key, self.negated_message(key))
                    else:
                        self.error(key, self.message(key))

                continue
            if not self.passes(self.find(key, dictionary), key, dictionary):
                boolean = False
                self.error(key, self.message(key))

        return boolean


class required(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute

    def message(self, key):
        return '{} is required'.format(key)


class accepted(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is True or attribute == 'on' or attribute == 'yes' or attribute == '1' or attribute == 1

    def message(self, attribute):
        return '{} terms must be yes, on, 1 or true'.format(attribute)


class numeric(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return str(attribute).isdigit()

    def message(self, attribute):
        return '{} must be a numeric'.format(attribute)


class string(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return isinstance(attribute, str)

    def message(self, attribute):
        return '{} must be a string'.format(attribute)


class none(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is None

    def message(self, attribute):
        return '{} must be None'.format(attribute)


class length(BaseValidation):

    def __init__(self, validations, min=1, max=999999, messages={}):
        super().__init__(validations, messages=messages)
        if isinstance(min, str) and '..' in min:
            self.min = int(min.split('..')[0])
            self.max = int(min.split('..')[1])
        else:
            self.min = min
            self.max = max

    def passes(self, attribute, key, dictionary):
        return len(str(attribute)) >= self.min and len(str(attribute)) <= self.max

    def message(self, attribute):
        return '{} length must be between {} and {}'.format(attribute, self.min, self.max)

    def negated_message(self, attribute):
        return '{} length must not be between {} and {}'.format(attribute, self.min, self.max)


class in_range(BaseValidation):

    def __init__(self, validations, min=1, max=255, messages={}):
        super().__init__(validations, messages=messages)
        self.min = min
        self.max = max

    def passes(self, attribute, key, dictionary):
        return attribute >= self.min and attribute <= self.max

    def message(self, attribute):
        return '{} must be between {} and {}'.format(attribute, self.min, self.max)

    def negated_message(self, attribute):
        return '{} must not be between {} and {}'.format(attribute, self.min, self.max)


class equals(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute == self.value

    def message(self, attribute):
        return '{} must be equal to {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not be equal to {}'.format(attribute, self.value)

class contains(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return self.value in attribute

    def message(self, attribute):
        return '{} must contain {}'.format(attribute, self.value)


class is_in(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute in self.value

    def message(self, attribute):
        return '{} must contain an element in {}'.format(attribute, self.value)


class greater_than(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute > self.value

    def message(self, attribute):
        return '{} must be greater than {}'.format(attribute, self.value)


class less_than(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute < self.value

    def message(self, attribute):
        return '{} must be less than {}'.format(attribute, self.value)


class isnt(BaseValidation):

    def __init__(self, *rules, messages={}):
        super().__init__(rules)

    def handle(self, dictionary):
        for rule in self.validations:
            rule.negate().handle(dictionary)
            self.errors += rule.errors


class when(BaseValidation):

    def __init__(self, *rules, messages={}):
        super().__init__(rules)
        self.should_run_then = True

    def handle(self, dictionary):
        self.dictionary = dictionary
        for rule in self.validations:
            if not rule.handle(dictionary):
                self.errors += rule.errors

        if not self.errors:
            for rule in self.then_rules:
                if not rule.handle(dictionary):
                    self.errors += rule.errors

    def then(self, *rules):
        self.then_rules = rules
        return self


class truthy(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute

    def message(self, attribute):
        return '{} must be a truthy value'.format(attribute)


class json(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import json
        try:
            return json.loads(attribute)
        except (TypeError, json.decoder.JSONDecodeError):
            return False

    def message(self, attribute):
        return '{} must be json'.format(attribute)


class Validator:

    def __init__(self, dictionary, *rules):
        self.errors = []
        self.validate(dictionary, *rules)

    def validate(self, dictionary, *rules):
        for rule in rules:
            rule.handle(dictionary)
            self.errors += rule.errors
