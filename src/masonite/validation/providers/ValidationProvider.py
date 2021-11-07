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

        MessageBag.get_errors = self._get_errors
        self.application.make("view").share({"bag": MessageBag.view_helper})
        validator.extend(ValidationFactory().registry)

    def boot(self):
        pass

    def _get_errors(self):
        request = self.application.make("request")
        messages = []
        for error, message in (
            request.session.get_flashed_messages().get("errors", {}).items()
        ):
            messages += message

        return messages
