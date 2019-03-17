from cleo import Command

from masonite.app import App
from masonite.helpers.filesystem import make_directory
from masonite.view import View


class BaseScaffoldCommand(Command):
    """
    Creates a model.

    model
        {name : Name of the model}
    """

    scaffold_name = 'Example'
    suffix = ''
    postfix = ''
    file_extension = '.py'
    base_directory = 'app/example/'

    template = '/masonite/snippets/scaffold/model'

    def handle(self):
        class_name = self.argument('name') + self.postfix
        view = View(App())
        class_directory = '{}{}{}{}'.format(
            self.base_directory, class_name, self.suffix, self.file_extension)

        if not make_directory(class_directory):
            return self.error('{0} Already Exists!'.format(self.scaffold_name))

        f = open(class_directory, 'w+')
        if view.exists(self.template):
            f.write(
                view.render(self.template, {
                            'class': class_name.split('/')[-1]}).rendered_template
            )
            self.info('{} Created Successfully!'.format(self.scaffold_name))
            return f.close()
