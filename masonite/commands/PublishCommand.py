"""Publish Service Providers"""
from cleo import Command


class PublishCommand(Command):
    """
    Publishes a Service Provider

    publish
        {name : Name of the Service Provider you want to publish}
        {--t|tag=None : The tag of the provider you want to publish}
    """

    def handle(self):
        from wsgi import container

        for provider in container.make('Providers'):
            if provider.__class__.__name__ == self.argument('name'):
                if self.option('tag') != 'None':
                    provider.publish(tag=self.option('tag'))
                    provider.publish_migrations(tag=self.option('tag'))

                provider.publish()
                provider.publish_migrations()

                return

        raise ValueError('Could not find the {} provider'.format(self.argument('name')))
