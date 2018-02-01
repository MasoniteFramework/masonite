''' Core of the IOC Container '''
import inspect

class App():
    ''' Core of the Service Container. Performs bindings and resolving
        of objects to and from the container.
    '''

    def __init__(self):
        self.providers = {}

    def bind(self, name, class_obj):
        ''' Bind classes into the container with a key value pair '''
        self.providers.update({name: class_obj})
        return self

    def make(self, name):
        ''' Retreives a class from the container by key '''
        return self.providers[name]

    def resolve(self, obj):
        ''' Takes a function or class method and resolves it's parameters
            from classes in the container
        '''

        provider_list = []
        for provider in inspect.signature(obj).parameters:
            if provider is not 'self' and provider not in inspect.getfullargspec(obj)[6]:
                provider_list.append(self.providers[provider])

        if inspect.getfullargspec(obj)[6]:
            provider_list = self.resolve_annotations(obj, provider_list)

        try:
            return obj(*provider_list)
        except TypeError:
            raise TypeError('Could not resolve the incorrect amount of objects from the container')

    def resolve_annotations(self, obj, provider_list):
        ''' Resolves class annotations (type hinting) parameters.
            Will retrieve by class type.
        '''
        for parameter in inspect.signature(obj).parameters.values():
            if parameter.annotation:
                for provider, provider_class in self.providers.items():
                    if parameter.annotation == provider_class.__class__ or parameter.annotation == provider_class:
                        provider_list.append(provider_class)

        return provider_list
