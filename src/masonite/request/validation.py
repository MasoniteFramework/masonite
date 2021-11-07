from ..validation import Validator


class ValidatesRequest:
    def validate(self, *rules):
        validator = Validator()
        return validator.validate(self.all(), *rules)
