"""New Model Command."""

from masonite.commands import BaseScaffoldCommand


class RuleEnclosureCommand(BaseScaffoldCommand):
    """
    Creates a new Rule.

    rule:enclosure
        {name : Name of the rule enclosure}
    """

    scaffold_name = 'Rule'
    postfix = ""
    template = '/masonite/snippets/scaffold/rule_enclosure'
    base_directory = 'app/rules/'
