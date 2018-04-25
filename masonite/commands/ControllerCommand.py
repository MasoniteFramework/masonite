from cleo import Command
import os


class ControllerCommand(Command):
    """
    Creates a controller

    controller
        {name : Name of the view you would like to create}
    """

    def handle(self):
        controller = self.argument('name')
        if os.path.isfile('app/http/controllers/{0}.py'.format(controller)):
            self.error('{0} Controller Exists!'.format(controller))
        else:
            f = open('app/http/controllers/{0}.py'.format(controller), 'w+')
            f.write("''' A Module Description '''\n\n")
            f.write('class {0}:\n'.format(controller))
            f.write("    ''' Class Docstring Description '''\n\n")
            f.write('    def show(self):\n')
            f.write('        pass\n')

            self.info('{0} Created Successfully!'.format(controller))
