from cleo import Command

from ..app import App
from ..helpers.filesystem import make_directory
from ..view import View


class BaseScaffoldCommand(Command):
    """
    Creates a model.

    model
        {name : Name of the model}
    """

    scaffold_name = 'Example'
    suffix = ''
    postfix = ''
    prefix = ''
    file_extension = '.py'
    base_directory = 'app/example/'
    file_to_lower = False

    template = '/masonite/snippets/scaffold/model'

    def handle(self):
        # If postfix already exists as part of the name, don't add it again
        if self.postfix and self.argument("name").lower().endswith(self.postfix.lower()):
            class_name = self.argument("name")
        else:
            class_name = self.argument("name") + self.postfix

        view = View(App())
        class_directory = '{}{}{}{}'.format(
            self.base_directory, class_name, self.suffix, self.file_extension)

        if self.file_to_lower:
            class_directory = class_directory.lower()

        if not make_directory(class_directory):
            return self.error('{0} Already Exists!'.format(self.scaffold_name))

        with open(class_directory, 'w+') as f:
            if view.exists(self.template):
                f.write(
                    view.render(self.template, {
                                'class': self.prefix + class_name.split('/')[-1]}).rendered_template
                )
                self.info('{} Created Successfully!'.format(self.scaffold_name))
