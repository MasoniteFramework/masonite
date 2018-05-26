from pydoc import importlib
import pkgutil
import inspect
from masonite.exceptions import InvalidAutoloadPath


class Autoload:

    def __init__(self, app):
        self.app = app

    def load(self, directories):     
        for (module_loader, name, ispkg) in pkgutil.iter_modules(directories):
            search_path = module_loader.path
            if search_path.endswith('/'):
                raise InvalidAutoloadPath('Autoload path cannot have a trailing slash')
                
            mod = importlib.import_module(module_loader.path.replace('/', '.') + '.' + name)
            for obj in inspect.getmembers(mod):
                if inspect.isclass(obj[1]):
                    self.app.bind(obj[1].__name__, obj[1])