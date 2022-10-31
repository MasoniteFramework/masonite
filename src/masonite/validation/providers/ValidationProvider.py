"""A Validation Service Provider."""
from ...providers import Provider
from .. import Validator, ValidationFactory, MessageBag
from ..commands.MakeRuleEnclosureCommand import MakeRuleEnclosureCommand
from ..commands.MakeRuleCommand import MakeRuleCommand


class ValidationProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        validator = Validator()
        self.application.bind("validator", validator)
        self.application.make("commands").add(
            MakeRuleEnclosureCommand(self.application),
            MakeRuleCommand(self.application),
        )

        validator.extend(ValidationFactory().registry)

    def boot(self):
        pass
