''' Core of the IOC Container '''
import inspect

class App():

    def __init__(self):
        self.providers = {}

    def bind(self, name, class_obj):
        self.providers.update({name: class_obj})
        return self

    def make(self, name):
        return self.providers[name]

    def resolve(self, obj):
        provider_list = []
        for provider in inspect.getargspec(obj)[0]:
            if provider is not 'self':
                provider_list.append(self.providers[provider])

        return obj(*provider_list)


