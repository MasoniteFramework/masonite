"""New Providers Command."""
from masonite.commands import BaseScaffoldCommand


class ProviderCommand(BaseScaffoldCommand):
    """
    Creates a new Service Provider.

    provider
        {name : Name of the Service Provider you want to create}
    """

    scaffold_name = 'Service Provider'
    base_directory = 'app/providers/'
    template = '/masonite/snippets/scaffold/provider'
