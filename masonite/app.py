""" Core of the IOC Container """

import inspect
from masonite.exceptions import MissingContainerBindingNotFound, ContainerError, StrictContainerException


class App():
    """
    Core of the Service Container. Performs bindings and resolving
    of objects to and from the container.
    """

    def __init__(self, strict=False, override=True):
        self.providers = {}
        self.strict = strict
        self.override = override
        self._hooks = {
            'make': {},
            'bind': {},
            'resolve': {},
        }


    def bind(self, name, class_obj):
        """ 
        Bind classes into the container with a key value pair
        """
        if self.strict and name in self.providers:
            raise StrictContainerException('You cannot override a key inside a strict container')

        if self.override or not name in self.providers:
            self.fire_hook('bind', name, class_obj)
            self.providers.update({name: class_obj})

        return self


    def make(self, name):
        """
        Retreives a class from the container by key
        """
        if self.has(name):
            obj = self.providers[name]
            self.fire_hook('make', name, obj)
            return obj

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

    def collect(self, search):
        provider_list = {}
        if isinstance(search, str):
            # Search Can Be:
            #    '*ExceptionHook'
            #    'Sentry*'
            #    'Sentry*Hook'
            for key, value in self.providers.items():
                if search.startswith('*'):
                    if key.endswith(search.split('*')[1]):
                        provider_list.update({key: value})
                elif search.endswith('*'):
                    if key.startswith(search.split('*')[0]):
                        provider_list.update({key: value})
                elif '*' in search:
                    split_search = search.split('*')
                    if key.startswith(split_search[0]) and key.endswith(split_search[1]):
                        provider_list.update({key: value})
                else:
                    raise AttributeError("There is no '*' in your collection search")
        else:
            for provider_key, provider_class in self.providers.items():
                if inspect.isclass(provider_class) and issubclass(provider_class, search):
                    provider_list.update({provider_key: provider_class})
                    
        return provider_list

    def _find_parameter(self, parameter):
        """
        Find a parameter in the container
        """
        parameter = str(parameter)
        if parameter is not 'self' and parameter in self.providers:
            obj = self.providers[parameter]
            self.fire_hook('resolve', parameter, obj)
            return obj
        
        raise ContainerError(
            'The dependency with the key of {0} could not be found in the container'.format(parameter)
        )


    def _find_annotated_parameter(self, parameter):
        """
        Find a given annotation in the container
        """
        for provider, provider_class in self.providers.items():

            if parameter.annotation == provider_class or parameter.annotation == provider_class.__class__:
                obj = provider_class
                self.fire_hook('resolve', parameter, obj)
                return obj
            elif inspect.isclass(provider_class) and issubclass(provider_class, parameter.annotation):
                obj = provider_class
                self.fire_hook('resolve', parameter, obj)
                return obj
        
        raise ContainerError('The dependency with the {0} annotation could not be resolved by the container'.format(parameter))

    def on_bind(self, key, obj):
        return self._bind_hook('bind', key, obj)

    def on_make(self, key, obj):
        return self._bind_hook('make', key, obj)
    
    def on_resolve(self, key, obj):
        return self._bind_hook('resolve', key, obj)
    
    def fire_hook(self, action, key, obj):
        for hook, hook_list in self._hooks[action].items():
            for hook_obj in hook_list:
                hook_obj(obj, self)

    def _bind_hook(self, hook, key, obj):
        if key in self._hooks[hook]:
            self._hooks[hook][key].append(obj)
        else:
            self._hooks[hook].update({key: [obj]})
        return self
