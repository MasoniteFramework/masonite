"""New Model Command."""
from masonite.app import App
from masonite.helpers.filesystem import make_directory
from masonite.view import View

from cleo import Command


class ModelCommand(Command):
    """
    Creates a model.

    model
        {name : Name of the model}
        {--m|migration : Create a migration for specified model}
        {--s|seed=? : Create a database seed}
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

        with open(class_directory, 'w+') as f:
            if view.exists(self.template):
                f.write(
                    view.render(self.template, {
                                'class': class_name.split('/')[-1]}).rendered_template
                )
                self.info('{} Created Successfully!'.format(self.scaffold_name))

        if self.option('migration'):
            model_name = class_name.lower() + 's'
            self.call('migration', [
                ('name', 'create_{}_table'.format(model_name)),
                ('-c', model_name)
            ])

        if self.option('seed'):
            seed_file = model_name
            seed_file = self.option('seed')

            self.call('seed', [
                ('table', seed_file)
            ])
