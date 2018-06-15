from pydoc import importlib
import pkgutil
import inspect
from masonite.exceptions import InvalidAutoloadPath, AutoloadContainerOverwrite, ContainerError


class Autoload:

    classes = {}

    def __init__(self, app=None):
        self.app = app

    def load(self, directories, instantiate=False):
        self.instantiate = instantiate
        if not self.app:
            raise ContainerError('Container not specified. Pass the container into the constructor')

        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):

                # If the object is a class and the objects module starts with the search path
                if inspect.isclass(obj[1]) and obj[1].__module__.startswith(search_path.replace('/', '.')):
                    if self.app.has(obj[1].__name__) and not self.app.make(obj[1].__name__).__module__.startswith(search_path):
                        raise AutoloadContainerOverwrite(
                            'Container already has the key: {}. Cannot overwrite a container key that exists outside of your application.'.format(obj[1].__name__))
                    self.app.bind(obj[1].__name__, self._can_instantiate(obj))
    
    def instances(self, directories, instance, only_app=True, instantiate=False):
        self.instantiate = instantiate

        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):
                if inspect.isclass(obj[1]) and issubclass(obj[1], instance):
                    if only_app and obj[1].__module__.startswith(search_path.replace('/', '.')):
                        self.classes.update({obj[1].__name__: self._can_instantiate(obj)})
                    elif not only_app:
                        self.classes.update({obj[1].__name__: self._can_instantiate(obj)})

        return self.classes
    
    def collect(self, directories, only_app=True, instantiate=False):
        self.instantiate = instantiate

        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            
            for obj in inspect.getmembers(self._get_module_members(module_loader, name)):
                if inspect.isclass(obj[1]):
                    if only_app and obj[1].__module__.startswith(search_path.replace('/', '.')): 
                        self.classes.update({obj[1].__name__: self._can_instantiate(obj)})
                    elif not only_app:
                        self.classes.update({obj[1].__name__: self._can_instantiate(obj)})

        return self.classes

    def _can_instantiate(self, obj):
        if self.instantiate:
            return obj[1]()
        
        return obj[1]

    def _get_module_members(self, module_loader, name):
        search_path = module_loader.path
        if search_path.endswith('/'):
            raise InvalidAutoloadPath(
                'Autoload path cannot have a trailing slash')

        return importlib.import_module(
            module_loader.path.replace('/', '.') + '.' + name)
