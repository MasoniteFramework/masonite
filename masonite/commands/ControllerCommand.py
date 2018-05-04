from cleo import Command
import os


class ControllerCommand(Command):
    """
    Creates a controller

    controller
        {name : Name of the controller you would like to create}
        {--r|--resource : Create a controller as a resource}
        {--e|--exact : For add the name controller without `Controller` text}
    """

    def handle(self):
        controller = self.argument('name')

        if not self.option('exact'):
            controller = controller + "Controller"

        if os.path.isfile('app/http/controllers/{0}.py'.format(controller)):
            self.error('{0} Controller Exists!'.format(controller))
        else:
            f = open('app/http/controllers/{0}.py'.format(controller), 'w+')
            f.write("''' A Module Description '''\n\n")
            f.write('class {0}:\n'.format(controller))
            f.write("    ''' Class Docstring Description '''\n\n")
            f.write('    def show(self):\n')
            f.write('        pass\n')

            if self.option('resource'):
                f.write('\n    def index(self):\n')
                f.write('        pass\n\n')
                f.write('    def create(self):\n')
                f.write('        pass\n\n')
                f.write('    def store(self):\n')
                f.write('        pass\n\n')
                f.write('    def edit(self):\n')
                f.write('        pass\n\n')
                f.write('    def update(self):\n')
                f.write('        pass\n\n')
                f.write('    def destroy(self):\n')
                f.write('        pass\n')

            self.info('{0} Created Successfully!'.format(controller))
