class Required:
    error = "The element in required"

    def handle(self, key, dictionary, negation=False):
        if negation:
            return True

        return key in dictionary


class Numeric:
    error = "The element should be a numeric element"

    def handle(self, key, dictionary, negation=False):
        return key in dictionary and str(dictionary[key]).isdigit()

class JSONValidator:
    error = "The element needs to be a JSON object"

    def handle(self, key, dictionary, negation=False):
        import json
        try:
            return key in dictionary and json.loads(dictionary[key])
        except TypeError:
            return True if negation else False



class Validator:
    validations = {
        'required': Required,
        'numeric': Numeric,
        'json': JSONValidator,
    }

    def __init__(self, dictionary, rules):
        self.errors = {}
        self.validate(dictionary, rules)

    def validate(self, dictionary, rules):
        self.rules = rules

        for key, r in rules.items():
            split_rules = r.split('|')
            for rule in split_rules:
                x = self.validations[rule.replace('not_', '')]()

                if not x.handle(key, dictionary, negation=rule.startswith('not_')):
                    self.errors.update({key: x.error})
