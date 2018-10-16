import os
from cleo import Command


class ViewCommand(Command):
    """
    Creates a view

    view
        {name : Name of the view you would like to create}
    """

    def handle(self):
        name = self.argument('name')
        if not os.path.isfile('resources/templates/' + name + '.html'):
            if not os.path.exists(os.path.dirname('resources/templates/{0}.html'.format(name))):
                os.makedirs(os.path.dirname('resources/templates/{0}.html'.format(name)))
            open('resources/templates/' + name + '.html', 'w+')
            self.info('{0} View Created Successfully!'.format(name))
        else:
            self.error('{0} View Exists!'.format(name))
