"""New Validator Command."""
from masonite.commands import BaseScaffoldCommand


class ValidatorCommand(BaseScaffoldCommand):
    """
    Creates a validator.

    validator
        {name : Name of the validator}
    """

    scaffold_name = 'Validator'
    base_directory = 'app/validators/'
    template = '/masonite/snippets/scaffold/validator'
