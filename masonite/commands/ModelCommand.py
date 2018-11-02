"""New Model Command."""
from masonite.commands import BaseScaffoldCommand


class ModelCommand(BaseScaffoldCommand):
    """
    Creates a model.

    model
        {name : Name of the model}
    """

    scaffold_name = "Model"
    template = '/masonite/snippets/scaffold/model'
    base_directory = 'app/'
