from typing import TYPE_CHECKING
from ..validation import Validator

if TYPE_CHECKING:
    from ..validation import RuleEnclosure, MessageBag


class ValidatesRequest:
    """Request mixin to add inputs validation to requests."""

    def validate(self, *rules: "str|dict|RuleEnclosure") -> "MessageBag":
        """Validate request inputs against the given rules."""
        validator = Validator()
        return validator.validate(self.all(), *rules)
