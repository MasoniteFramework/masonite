import os
from cleo import Command


class ProviderCommand(Command):
    """
    Creates a new Service Provider

    provider
        {name : Name of the Service Provider you want to create}
    """

    def handle(self):
        provider = self.argument('name')

        if not os.path.isfile('app/providers/{0}.py'.format(provider)):
            if not os.path.exists(os.path.dirname('app/providers/{0}.py'.format(provider))):
                # Create the path to the service provider if it does not exist
                os.makedirs(os.path.dirname('app/providers/{0}.py'.format(provider)))

            f = open('app/providers/{0}.py'.format(provider), 'w+')

            f.write("''' A {0} Service Provider '''\n".format(provider))
            f.write('from masonite.provider import ServiceProvider\n\n')
            f.write("class {0}(ServiceProvider):\n\n    ".format(provider))
            f.write("def register(self):\n        pass\n\n    ")
            f.write("def boot(self):\n        pass\n")

            self.info('Service Provider Created Successfully!')
        else:
            self.comment('Service Provider Already Exists!')
