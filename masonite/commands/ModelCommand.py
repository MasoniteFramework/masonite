"""New Model Command."""
import subprocess

from masonite.app import App
from masonite.helpers.filesystem import make_directory
from masonite.view import View

from cleo import Command


class ModelCommand(Command):
    """
    Creates a model.

    model
        {name : Name of the model}
        {--m|--migration : Create a migration for specified model}
    """

    scaffold_name = "Model"
    template = '/masonite/snippets/scaffold/model'
    base_directory = 'app/'

    def handle(self):
        class_name = self.argument('name')
        view = View(App())
        class_directory = '{}{}.py'.format(self.base_directory, class_name)

        if not make_directory(class_directory):
            return self.error('{0} Already Exists!'.format(self.scaffold_name))

        f = open(class_directory, 'w+')
        if view.exists(self.template):
            f.write(
                view.render(self.template, {
                            'class': class_name.split('/')[-1]}).rendered_template
            )
            self.info('{} Created Successfully!'.format(self.scaffold_name))
            f.close()

        if self.option('migration'):
            model_name = class_name.lower() + 's'
            subprocess.call(['orator', 'make:migration', 'create_{}_table'.format(model_name),
                             '-p', 'databases/migrations', '--table',
                             model_name, '--create'])
