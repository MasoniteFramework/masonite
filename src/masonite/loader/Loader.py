"""Loader class to easily list, find or load any object in a given module, or folder."""
import inspect
import pkgutil
import os

from ..exceptions import LoaderNotFound
from ..utils.str import as_filepath
from ..utils.structures import load


def parameters_filter(obj_name, obj):
    return (
        obj_name.isupper()
        and not obj_name.startswith("__")
        and not obj_name.endswith("__")
    )


class Loader:
    def get_modules(self, files_or_directories, raise_exception=False):
        if not isinstance(files_or_directories, list):
            files_or_directories = [files_or_directories]

        _modules = {}
        module_paths = list(map(as_filepath, files_or_directories))
        for module_loader, name, _ in pkgutil.iter_modules(module_paths):
            module = load(
                f"{os.path.relpath(module_loader.path)}.{name}",
                raise_exception=raise_exception,
            )
            _modules.update({name: module})
        return _modules

    def find(self, class_instance, paths, class_name, raise_exception=False):
        _classes = self.find_all(class_instance, paths)
        for name, obj in _classes.items():
            if name == class_name:
                return obj
        if raise_exception:
            raise LoaderNotFound(
                f"No {class_instance} named {class_name} has been found in {paths}"
            )
        return None

    def find_all(self, class_instance, paths, raise_exception=False):
        _classes = {}
        for module in self.get_modules(paths).values():
            for obj_name, obj in inspect.getmembers(module):
                # check if obj is the same class as the given one
                if inspect.isclass(obj) and issubclass(obj, class_instance):
                    # check if the class really belongs to those paths to load internal only
                    if obj.__module__.startswith(module.__package__):
                        _classes.update({obj_name: obj})
        if not len(_classes.keys()) and raise_exception:
            raise LoaderNotFound(f"No {class_instance} have been found in {paths}")
        return _classes

    def get_object(self, path_or_module, object_name, raise_exception=False):
        return load(path_or_module, object_name, raise_exception=raise_exception)

    def get_objects(self, path_or_module, filter_method=None, raise_exception=False):
        """Returns a dictionary of objects from the given path (file or dotted). The dictionary can
        be filtered if a given callable is given."""
        if isinstance(path_or_module, str):
            module = load(path_or_module, raise_exception=raise_exception)
        else:
            module = path_or_module
        if not module:
            return None
        return dict(inspect.getmembers(module, filter_method))

    def get_parameters(self, module_or_path):
        _parameters = {}
        for name, obj in self.get_objects(module_or_path).items():
            if parameters_filter(name, obj):
                _parameters.update({name: obj})

        return _parameters
