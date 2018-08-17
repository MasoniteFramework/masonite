from cleo import Command
import os
from masonite.view import View
from masonite.app import App
from masonite.helpers.filesystem import make_directory

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
        view = View(App())

        if not self.option('exact'):
            controller = controller + "Controller"

        if not make_directory('app/http/controllers/{0}.py'.format(controller)):
            return self.error('{0} Controller Exists!'.format(controller))
            

        f = open('app/http/controllers/{0}.py'.format(controller), 'w+')
        if view.exists('/masonite/snippets/scaffold/controller'):
            if self.option('resource'):
                f.write(
                    view.render('/masonite/snippets/scaffold/controller_resource',
                                {'class': controller.split('/')[-1]}).rendered_template
                )
            else:
                f.write(
                    view.render('/masonite/snippets/scaffold/controller',
                                {'class': controller.split('/')[-1]}).rendered_template
                )
            self.info('Controller Created Successfully!')
            return f.close()

        # f.write("''' A Module Description '''\n\n")
        # f.write('class {0}:\n'.format(controller))
        # f.write("    ''' Class Docstring Description '''\n\n")
        # f.write('    def show(self):\n')
        # f.write('        pass\n')


        #         f.write('\n    def index(self):\n')
        #         f.write('        pass\n\n')
        #         f.write('    def create(self):\n')
        #         f.write('        pass\n\n')
        #         f.write('    def store(self):\n')
        #         f.write('        pass\n\n')
        #         f.write('    def edit(self):\n')
        #         f.write('        pass\n\n')
        #         f.write('    def update(self):\n')
        #         f.write('        pass\n\n')
        #         f.write('    def destroy(self):\n')
        #         f.write('        pass\n')

        #     self.info('{0} Created Successfully!'.format(controller))
