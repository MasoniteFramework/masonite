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
        """The passing criteria for this rule. 

        This should return a True boolean value.

        Arguments:
            attribute {mixed} -- The value found within the dictionary
            key {string} -- The key in the dictionary being searched for. 
                            This key may or may not exist in the dictionary.
            dictionary {dict} -- The dictionary being searched

        Returns:
            bool
        """
        return attribute

    def message(self, key):
        """A message to show when this rule fails

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return '{} is required'.format(key)

    def negated_message(self, key):
        """A message to show when this rule is negated using a negation rule like 'isnt()'

        For example if you have a message that says 'this is required' you may have a negated statement
        that says 'this is not required'.

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return '{} is not required'.format(key)


class accepted(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is True or attribute == 'on' or attribute == 'yes' or attribute == '1' or attribute == 1

    def message(self, attribute):
        return '{} must be yes, on, 1 or true'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be yes, on, 1 or true'.format(attribute)


class numeric(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return str(attribute).isdigit()

    def message(self, attribute):
        return '{} must be a numeric'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a numeric'.format(attribute)


class string(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return isinstance(attribute, str)

    def message(self, attribute):
        return '{} must be a string'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a string'.format(attribute)


class none(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is None

    def message(self, attribute):
        return '{} must be None'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be None'.format(attribute)


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

    def negated_message(self, attribute):
        return '{} must not contain {}'.format(attribute, self.value)


class is_in(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute in self.value

    def message(self, attribute):
        return '{} must contain an element in {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not contain an element in {}'.format(attribute, self.value)


class greater_than(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute > self.value

    def message(self, attribute):
        return '{} must be greater than {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must be greater than {}'.format(attribute, self.value)


class less_than(BaseValidation):

    def __init__(self, validations, value='', messages={}):
        super().__init__(validations, messages=messages)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute < self.value

    def message(self, attribute):
        return '{} must be less than {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not be less than {}'.format(attribute, self.value)


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

    def negated_message(self, attribute):
        return '{} must not be a truthy value'.format(attribute)


class json(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import json
        try:
            return json.loads(attribute)
        except (TypeError, json.decoder.JSONDecodeError):
            return False

    def message(self, attribute):
        return '{} must be json'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be json'.format(attribute)


class Validator:

    def __init__(self):
        self.errors = []

    def validate(self, dictionary, *rules):
        for rule in rules:
            rule.handle(dictionary)
            self.errors += rule.errors

        return self

    def extend(self, key, obj=None):
        if isinstance(key, dict):
            self.__dict__.update(key)
            return self

        self.__dict__.update({key: obj})
        return self

    def register(self, *cls):
        for obj in cls:
            self.__dict__.update({
                obj.__name__: obj
            })


class ValidationFactory:

    registry = {}

    def __init__(self):
        self.register(
            required,
            json,
            accepted,
            numeric,
            string,
            none,
            in_range,
            length,
            equals,
            contains,
            is_in,
            greater_than,
            less_than,
            isnt,
            when,
            truthy,
            json
        )

    def register(self, *cls):
        for obj in cls:
            self.registry.update({
                obj.__name__: obj
            })
