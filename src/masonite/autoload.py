"""Autoloader Module.

This contains the class for autoloading classes from directories.
This class is simply used to point at a directory and retrieve all classes in that directory.
"""

import inspect
import pkgutil
from pydoc import importlib

from masonite.exceptions import (AutoloadContainerOverwrite, ContainerError,
                                 InvalidAutoloadPath)


class Autoload:
    """Autoload class. Used to retrieve all classes from any set of directories."""

    classes = {}

    def __init__(self, app=None):
        """Autoload Constructor.

        Keyword Arguments:
            app {masonite.app.App} -- Container class (default: {None})
        """
        self.app = app

    def load(self, directories, instantiate=False):
        """Load all classes found in a list of directories into the container.

        Arguments:
            directories {list} -- List of directories to search.

        Keyword Arguments:
            instantiate {bool} -- Whether or not to instantiate the class (default: {False})

        Raises:
            ContainerError -- Thrown when the container is not loaded into the class.
            AutoloadContainerOverwrite -- Thrown when the container already has the key binding.
        """
        self.instantiate = instantiate
        if not self.app:
            raise ContainerError(
                'Container not specified. Pass the container into the constructor')

        for (module_loader, name, _) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):

                # If the object is a class and the objects module starts with the search path
                if inspect.isclass(obj[1]) and obj[1].__module__.split('.')[:-1] == search_path.split('/'):
                    if self.app.has(obj[1].__name__) and not self.app.make(obj[1].__name__).__module__.startswith(search_path):
                        raise AutoloadContainerOverwrite(
                            'Container already has the key: {}. Cannot overwrite a container key that exists outside of your application.'.format(obj[1].__name__))
                    self.app.bind(obj[1].__name__, self._can_instantiate(obj))

    def instances(self, directories, instance, only_app=True, instantiate=False):
        """Use to autoload all instances of a specific object.

        Arguments:
            directories {list} -- List of directories to search.
            instance {object} -- Object to search for instances of.

        Keyword Arguments:
            only_app {bool} -- Only search in the current application namespace. This will not found other classes
                               that are imported through third party packages. (default: {True})
            instantiate {bool} -- Whether or not to instantiate the classes it finds. (default: {False})

        Returns:
            dict -- Returns a dictionary of classes it found.
        """
        self.instantiate = instantiate

        for (module_loader, name, _) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):
                if inspect.isclass(obj[1]) and issubclass(obj[1], instance):
                    if only_app and obj[1].__module__.startswith(search_path.replace('/', '.')):
                        self.classes.update(
                            {obj[1].__name__: self._can_instantiate(obj)})
                    elif not only_app:
                        self.classes.update(
                            {obj[1].__name__: self._can_instantiate(obj)})

        return self.classes

    def collect(self, directories, only_app=True, instantiate=False):
        """Collect all classes from a specific list of directories.

        Arguments:
            directories {list} -- List of directories to search.

        Keyword Arguments:
            only_app {bool} -- Only search in the current application namespace. This will not found other classes
                               that are imported through third party packages. (default: {True})
            instantiate {bool} -- Whether or not to instantiate the classes it finds. (default: {False})

        Returns:
            dict -- Returns a dictionary of objects found and their key bindings.
        """
        self.instantiate = instantiate

        for (module_loader, name, _) in pkgutil.iter_modules(directories):
            search_path = module_loader.path

            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):
                if inspect.isclass(obj[1]):
                    if only_app and obj[1].__module__.startswith(search_path.replace('/', '.')):
                        self.classes.update(
                            {obj[1].__name__: self._can_instantiate(obj)})
                    elif not only_app:
                        self.classes.update(
                            {obj[1].__name__: self._can_instantiate(obj)})

        return self.classes

    def _can_instantiate(self, obj):
        """Instantiate the class or not depending on the property set.

        Arguments:
            obj {object} -- Object to check for instantiation.

        Returns:
            object -- Returns the object being instantiated.
        """
        if self.instantiate:
            return obj[1]()

        return obj[1]

    def _get_module_members(self, module_loader, name):
        """Get the module members.

        Arguments:
            module_loader {pkgutil.ModuleLoader} -- Module Loader from the pkgutil library
            name {string} -- Name of the module

        Raises:
            InvalidAutoloadPath -- Thrown when the search path ends with a forward

        Returns:
            module -- returns the imported module.
        """
        search_path = module_loader.path
        if search_path.endswith('/'):
            raise InvalidAutoloadPath(
                'Autoload path cannot have a trailing slash')

        return importlib.import_module(
            module_loader.path.replace('/', '.') + '.' + name)
