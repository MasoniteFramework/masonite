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
        print(self.option('tag'))
        from config import providers

        for provider in providers.PROVIDERS:
            if provider.__name__ == self.argument('name'):
                if self.option('tag') != 'None':
                    provider().publish(tag=self.option('tag'))
                
                provider().publish()
                
                return
        
        raise ValueError('Could not find the {} provider'.format(self.argument('name')))

