from masonite.helpers import Dot as DictDot
from .RuleEnclosure import RuleEnclosure
import inspect
import re


class BaseValidation:

    def __init__(self, validations, messages={}, raises={}):
        self.errors = {}
        self.messages = messages
        if isinstance(validations, str):
            self.validations = [validations]
        else:
            self.validations = validations
        self.negated = False
        self.raises = raises

    def passes(self, attribute, key, dictionary):
        return True

    def error(self, key, message):
        if key in self.messages:
            if key in self.errors:
                self.errors[key].append(self.messages[key])
                return

            self.errors.update({key: [self.messages[key]]})
            return
        self.errors.update({key: [message]})

    def find(self, key, dictionary, default=False):
        return DictDot().dot(key, dictionary, default)

    def message(self, key):
        return ''

    def negate(self):
        self.negated = True
        return self

    def raise_exception(self, key):
        if self.raises is not True and key in self.raises:
            error = self.raises.get(key)
            raise error(self.errors[next(iter(self.errors))][0])

        raise ValueError(self.errors[next(iter(self.errors))][0])

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

            if self.errors and self.raises:
                return self.raise_exception(key)

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


class timezone(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import pytz
        return attribute in pytz.all_timezones

    def message(self, attribute):
        return '{} must be a valid timezone'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a valid timezone'.format(attribute)


class accepted(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is True or attribute == 'on' or attribute == 'yes' or attribute == '1' or attribute == 1

    def message(self, attribute):
        return '{} must be yes, on, 1 or true'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be yes, on, 1 or true'.format(attribute)


class ip(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import socket

        try:
            socket.inet_aton(attribute)
            return True
        except socket.error:
            return False

    def message(self, attribute):
        return '{} must be a valid ipv4 address'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a valid ipv4 address'.format(attribute)


class date(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            date = pendulum.parse(attribute)
            return date
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return '{} must be a valid date'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a valid date'.format(attribute)


class before_today(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz) <= pendulum.yesterday()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return '{} must be a date before today'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a date before today'.format(attribute)


class after_today(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz) >= pendulum.yesterday()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return '{} must be a date after today'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a date after today'.format(attribute)


class is_past(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz).is_past()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return '{} must be a time in the past'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a time in the past'.format(attribute)


class is_future(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz).is_future()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return '{} must be a time in the past'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a time in the past'.format(attribute)


class email(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return re.compile(r"^[^.].+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$").match(attribute)

    def message(self, attribute):
        return '{} must be a valid email address'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be a valid email address'.format(attribute)


class exists(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return key in dictionary

    def message(self, attribute):
        return '{} must exist'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not exist'.format(attribute)


class active_domain(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import socket
        try:
            if '@' in attribute:
                # validation is for an email address
                return socket.gethostbyname(
                    attribute.split('@')[1]
                )

            return socket.gethostbyname(
                attribute.replace('https://', '').replace('http://', '').replace('www.', '')
            )
        except socket.gaierror:
            return False

    def message(self, attribute):
        return '{} must be an active domain name'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be an active domain name'.format(attribute)


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

    def __init__(self, validations, min=1, max=999999, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
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

    def __init__(self, validations, min=1, max=255, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.min = min
        self.max = max

    def passes(self, attribute, key, dictionary):
        return attribute >= self.min and attribute <= self.max

    def message(self, attribute):
        return '{} must be between {} and {}'.format(attribute, self.min, self.max)

    def negated_message(self, attribute):
        return '{} must not be between {} and {}'.format(attribute, self.min, self.max)


class equals(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute == self.value

    def message(self, attribute):
        return '{} must be equal to {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not be equal to {}'.format(attribute, self.value)


class contains(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return self.value in attribute

    def message(self, attribute):
        return '{} must contain {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not contain {}'.format(attribute, self.value)


class is_in(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute in self.value

    def message(self, attribute):
        return '{} must contain an element in {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not contain an element in {}'.format(attribute, self.value)


class greater_than(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute > self.value

    def message(self, attribute):
        return '{} must be greater than {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must be greater than {}'.format(attribute, self.value)


class less_than(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute < self.value

    def message(self, attribute):
        return '{} must be less than {}'.format(attribute, self.value)

    def negated_message(self, attribute):
        return '{} must not be less than {}'.format(attribute, self.value)


class isnt(BaseValidation):

    def __init__(self, *rules, messages={}, raises={}):
        super().__init__(rules)

    def handle(self, dictionary):
        for rule in self.validations:
            rule.negate().handle(dictionary)
            self.errors.update(rule.errors)


class when(BaseValidation):

    def __init__(self, *rules, messages={}, raises={}):
        super().__init__(rules)
        self.should_run_then = True

    def handle(self, dictionary):
        self.dictionary = dictionary
        for rule in self.validations:
            if not rule.handle(dictionary):
                self.errors.update(rule.errors)

        if not self.errors:
            for rule in self.then_rules:
                if not rule.handle(dictionary):
                    self.errors.update(rule.errors)

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
        import json as json_module

        # Hacky workaround for Python 3.4
        try:
            JsonParseException = json.decoder.JSONDecodeError
        except AttributeError:
            JsonParseException = ValueError

        try:
            return json_module.loads(str(attribute))
        except (TypeError, JsonParseException):
            return False

    def message(self, attribute):
        return '{} must be json'.format(attribute)

    def negated_message(self, attribute):
        return '{} must not be json'.format(attribute)


class phone(BaseValidation):

    def __init__(self, *rules, pattern="123-456-7890", messages={}, raises={}):
        super().__init__(rules, messages={}, raises={})
        # 123-456-7890
        # (123)456-7890
        self.pattern = pattern

    def passes(self, attribute, key, dictionary):
        if self.pattern == '(123)456-7890':
            return re.compile(r"^\(\w{3}\)\w{3}\-\w{4}$").match(attribute)
        elif self.pattern == '123-456-7890':
            return re.compile(r"^\w{3}\-\w{3}\-\w{4}$").match(attribute)

    def message(self, attribute):
        if self.pattern == '(123)456-7890':
            return '{} must be in the format (XXX)XXX-XXXX'.format(attribute)
        elif self.pattern == '123-456-7890':
            return '{} must be in the format XXX-XXX-XXXX'.format(attribute)

    def negated_message(self, attribute):
        if self.pattern == '(123)456-7890':
            return '{} must not be in the format (XXX)XXX-XXXX'.format(attribute)
        elif self.pattern == '123-456-7890':
            return '{} must not be in the format XXX-XXX-XXXX'.format(attribute)


class Validator:

    def __init__(self):
        pass

    def validate(self, dictionary, *rules):
        rule_errors = {}
        try:
            for rule in rules:

                if inspect.isclass(rule) and isinstance(rule(), RuleEnclosure):
                    rule_errors.update(self.run_enclosure(rule(), dictionary))
                    continue

                rule.handle(dictionary)
                for error, message in rule.errors.items():
                    if error not in rule_errors:
                        rule_errors.update({error: message})
                    else:
                        messages = rule_errors[error]
                        messages += message
                        rule_errors.update({error: messages})

            return rule_errors

        except Exception as e:
            e.errors = rule_errors
            raise e

        return rule_errors

    def run_enclosure(self, enclosure, dictionary):
        rule_errors = {}
        for rule in enclosure.rules():
            for error, message in rule.errors.items():
                if error not in rule_errors:
                    rule_errors.update({error: message})
                else:
                    messages = rule_errors[error]
                    messages += message
                    rule_errors.update({error: messages})
        return rule_errors

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
            accepted,
            active_domain,
            after_today,
            before_today,
            contains,
            equals,
            email,
            exists,
            greater_than,
            in_range,
            is_future,
            is_in,
            isnt,
            is_past,
            ip,
            json,
            length,
            less_than,
            none,
            numeric,
            phone,
            required,
            string,
            timezone,
            truthy,
            when,
        )

    def register(self, *cls):
        for obj in cls:
            self.registry.update({
                obj.__name__: obj
            })
