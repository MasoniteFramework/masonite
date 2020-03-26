"""New Job Command."""
from ..commands import BaseScaffoldCommand


class MailableCommand(BaseScaffoldCommand):
    """
    Creates a new Mailable.

    mailable
        {name : Name of the job you want to create}
    """

    scaffold_name = 'Mailable'
    template = '/masonite/snippets/scaffold/mailable'
    base_directory = 'app/mailable/'
    postfix = "Mailable"
