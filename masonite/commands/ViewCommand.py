"""New View Command."""
from masonite.commands import BaseScaffoldCommand


class ViewCommand(BaseScaffoldCommand):
    """
    Creates a view.

    view
        {name : Name of the view you would like to create}
    """

    scaffold_name = "View"
    template = '/masonite/snippets/scaffold/view'
    file_extension = '.html'
    base_directory = 'resources/templates/'
