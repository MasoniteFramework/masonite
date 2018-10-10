"""New View Command."""
import os

from cleo import Command


class ViewCommand(Command):
    """
    Creates a view.

    view
        {name : Name of the view you would like to create}
    """

    def handle(self):
        name = self.argument('name')

        if os.path.isfile('resources/templates/{}.html'.format(name)):
            self.error('{} View Exists!'.format(name))
        else:
            open('resources/templates/{}.html'.format(name), 'w+')
            self.info('{} View Created Successfully!'.format(name))
