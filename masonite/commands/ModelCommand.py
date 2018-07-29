import os
from cleo import Command


class ModelCommand(Command):
    """
    Creates a model

    model
        {name : Name of the model}
    """

    def handle(self):
        model = self.argument('name')
        if not os.path.isfile('app/{0}.py'.format(model)):
            if not os.path.exists(os.path.dirname('app/{0}.py'.format(model))):
                # Create the path to the model if it does not exist
                os.makedirs(os.path.dirname('app/{0}.py'.format(model)))

            f = open('app/{0}.py'.format(model), 'w+')

            f.write("''' A {0} Database Model '''\n".format(
                model.split('/')[-1]))
            f.write('from config.database import Model\n\n')
            f.write("class {0}(Model):\n    pass\n".format(model.split('/')[-1]))

            self.info('Model Created Successfully!')
        else:
            self.error('Model Already Exists!')
