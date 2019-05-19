"""New Model Command."""

from masonite.commands import BaseScaffoldCommand


class RuleCommand(BaseScaffoldCommand):
    """
    Creates a new Rule.

    rule
        {name : Name of the rule}
    """

    scaffold_name = 'Rule'
    postfix = ""
    template = '/masonite/snippets/scaffold/rule'
    base_directory = 'app/rules/'
