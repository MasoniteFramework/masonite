""" Core of the IOC Container """

import inspect
from masonite.exceptions import MissingContainerBindingNotFound


class App():
    """
    Core of the Service Container. Performs bindings and resolving
    of objects to and from the container.
    """

    def __init__(self):
        self.providers = {}

    def bind(self, name, class_obj):
        """ Bind classes into the container with a key value pair """
        self.providers.update({name: class_obj})
        return self

    def make(self, name):
        """ Retreives a class from the container by key """
        if self.has(name):
            return self.providers[name]

        raise MissingContainerBindingNotFound("{0} key was not found in the container".format(name))

    def has(self, name):
        if name in self.providers:
            return True

        return False

    def helper(self):
        """ Adds a helper to create builtin functions """
        return self

    def resolve(self, obj):
        """
        Takes an object such as a function or class method and resolves it's 
        parameters from objects in the container
        """

        provider_list = []

        """
        Inspect all non annotation parameters, find them in the container
        and add them to the provider_list
        """
        for provider in inspect.signature(obj).parameters:
            if provider is not 'self' and provider not in inspect.getfullargspec(obj)[6]:
                provider_list.append(self.providers[provider])

        """
        Inspect all annotation parameters, find the object it annotates from the container
        and add the object to the provider_list
        """
        if inspect.getfullargspec(obj)[6]:
            provider_list = self.resolve_annotations(obj, provider_list)

        """
        Pass the provider list which contains all the dependencies found from the container
        into the parameters.
        """
        try:
            return obj(*provider_list)
        except TypeError:
            raise TypeError('Could not resolve the incorrect amount of objects from the container')

    def resolve_annotations(self, obj, provider_list):
        """
        Resolves class annotations (type hinted) parameters.
        This will retrieve the object from the container, not the key.
        """
        for parameter in inspect.signature(obj).parameters.values():
            if parameter.annotation:
                for provider, provider_class in self.providers.items():
                    if parameter.annotation == provider_class.__class__ or parameter.annotation == provider_class:
                        provider_list.append(provider_class)

        return provider_list
