import os
from cleo import Command


class ValidatorCommand(Command):
    """
    Creates a validator

    validator
        {name : Name of the validator}
    """

    def handle(self):
        validator = self.argument('name')
        if not os.path.isfile('app/validators/{0}.py'.format(validator)):
            if not os.path.exists(os.path.dirname('app/validators/{0}.py'.format(validator))):
                # Create the path to the validator if it does not exists already
                os.makedirs(os.path.dirname('app/validators/{0}.py'.format(validator)))

            f = open('app/validators/{0}.py'.format(validator), 'w+')

            f.write("''' A {0} Validator '''\n".format(validator.split('/')[-1]))
            f.write('from masonite.validator import Validator\n\n')
            f.write("class {0}Validator(Validator):\n    pass\n".format(validator.split('/')[-1]))

            self.info('Validator Created Successfully')
        else:
            self.error('Validator Already Exists!')
