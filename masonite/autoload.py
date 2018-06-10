from pydoc import importlib
import pkgutil
import inspect
from masonite.exceptions import InvalidAutoloadPath, AutoloadContainerOverwrite


class Autoload:

    classes = {}

    def __init__(self, app=None):
        self.app = app

    def load(self, directories):     
        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            if search_path.endswith('/'):
                raise InvalidAutoloadPath('Autoload path cannot have a trailing slash')
                
            mod = importlib.import_module(module_loader.path.replace('/', '.') + '.' + name)
            for obj in inspect.getmembers(mod):

                # If the object is a class and the objects module starts with the search path
                if inspect.isclass(obj[1]) and obj[1].__module__.startswith(search_path.replace('/', '.')):
                    if self.app.has(obj[1].__name__) and not self.app.make(obj[1].__name__).__module__.startswith(search_path):
                        raise AutoloadContainerOverwrite(
                            'Container already has the key: {}. Cannot overwrite a container key that exists outside of your application.'.format(obj[1].__name__))
                    self.app.bind(obj[1].__name__, obj[1])
    
    def instances(self, directories, instance):
        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            if search_path.endswith('/'):
                raise InvalidAutoloadPath('Autoload path cannot have a trailing slash')
                
            mod = importlib.import_module(module_loader.path.replace('/', '.') + '.' + name)
            for obj in inspect.getmembers(mod):
                if inspect.isclass(obj[1]) and issubclass(obj[1], instance):
                    self.classes.update({obj[1].__name__: obj[1]})

        return self
