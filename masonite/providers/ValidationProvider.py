"""A Validation Service Provider."""

from masonite.provider import ServiceProvider
from masonite.validation import Validator, ValidationFactory


class ValidationProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.singleton('Validator', Validator)

    def boot(self, validator: Validator):
        validator.extend(ValidationFactory().registry)
