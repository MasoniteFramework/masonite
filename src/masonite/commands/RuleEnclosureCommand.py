"""New Model Command."""

from ..commands import BaseScaffoldCommand


class RuleEnclosureCommand(BaseScaffoldCommand):
    """
    Creates a new rule enclosure.

    rule:enclosure
        {name : Name of the rule enclosure}
    """

    scaffold_name = 'Rule'
    postfix = ''
    template = '/masonite/validation/snippets/scaffold/rule_enclosure'
    base_directory = 'app/rules/'
