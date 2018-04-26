""" Core of the IOC Container """

import inspect
from masonite.exceptions import MissingContainerBindingNotFound, ContainerError


class App():
    """
    Core of the Service Container. Performs bindings and resolving
    of objects to and from the container.
    """

    def __init__(self):
        self.providers = {}


    def bind(self, name, class_obj):
        """ 
        Bind classes into the container with a key value pair
        """
        self.providers.update({name: class_obj})
        return self


    def make(self, name):
        """
        Retreives a class from the container by key
        """
        if self.has(name):
            return self.providers[name]

        raise MissingContainerBindingNotFound("{0} key was not found in the container".format(name))


    def has(self, name):
        """
        Check if a key exists in the container
        """
        if name in self.providers:
            return True

        return False


    def helper(self):
        """
        Adds a helper to create builtin functions
        """
        return self


    def resolve(self, obj):
        """
        Takes an object such as a function or class method and resolves it's 
        parameters from objects in the container
        """
        provider_list = []

        for parameter, value in inspect.signature(obj).parameters.items():
            if ':' in str(value):
                provider_list.append(self._find_annotated_parameter(value))
            else:
                provider_list.append(self._find_parameter(value))

        return obj(*provider_list)


    def _find_parameter(self, parameter):
        """
        Find a parameter in the container
        """
        parameter = str(parameter)
        if parameter is not 'self' and parameter in self.providers:
            return self.providers[parameter]
        
        raise ContainerError(
            'The dependency with the key of {0} could not be found in the container'.format(parameter)
        )


    def _find_annotated_parameter(self, parameter):
        """
        Find a given annotation in the container
        """
        for provider, provider_class in self.providers.items():
            if parameter.annotation == provider_class.__class__ or parameter.annotation == provider_class or isinstance(provider_class, parameter.annotation.__class__):
                return provider_class
        
        raise ContainerError('The dependency with the {0} annotation could not be resolved by the container'.format(parameter))
