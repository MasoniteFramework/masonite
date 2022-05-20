import inspect
import pkgutil
import os
from typing import Any, Callable, List

from ..exceptions import LoaderNotFound
from ..utils.str import as_filepath
from ..utils.structures import load


def parameters_filter(obj_name: str, obj: Any) -> bool:
    """Check if object is considered as a PEP-8 constant."""
    return (
        obj_name.isupper()
        and not obj_name.startswith("__")
        and not obj_name.endswith("__")
    )


class Loader:
    """Loader class to easily list, find or load any object in a given Python module or package."""

    def get_modules(
        self, files_or_directories: "str|List", raise_exception: bool = False
    ) -> dict:
        """Load a list of modules in given directory or directories. It returns a dictionary with
        module name as keys and loaded module as values. If raise_exception is enabled
        exceptions can be raised when an error happens when loading the module."""
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

    def find(
        self,
        class_instance: type,
        paths: "str|List",
        class_name: str,
        raise_exception: bool = False,
    ):
        _classes = self.find_all(class_instance, paths)
        for name, obj in _classes.items():
            if name == class_name:
                return obj
        if raise_exception:
            raise LoaderNotFound(
                f"No {class_instance} named {class_name} has been found in {paths}"
            )
        return None

    def find_all(
        self, class_instance: type, paths: "str|List", raise_exception: bool = False
    ):
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

    def get_object(
        self, path_or_module: str, object_name: str, raise_exception: bool = False
    ) -> Any:
        """Load the given object from a Python module located at path (can be a dotted path). If no
        object name is provided, loads the module. When raise_exception is enabled, exceptions can
        be raised if an error happens when loading the object.
        """
        return load(path_or_module, object_name, raise_exception=raise_exception)

    def get_objects(
        self,
        path_or_module: str,
        filter_method: "Callable" = None,
        raise_exception: bool = False,
    ) -> dict:
        """Returns a dictionary of objects from the given path (file or dotted). The dictionary can
        be filtered if a given callable is given. When raise_exception is enabled, exceptions can
        be raised if an error happens when loading the objects."""
        if isinstance(path_or_module, str):
            module = load(path_or_module, raise_exception=raise_exception)
        else:
            module = path_or_module
        if not module:
            return None
        return dict(inspect.getmembers(module, filter_method))

    def get_parameters(self, module_or_path: "str") -> dict:
        """Get parameters (constants) from the given module or Python path as a dictionary."""
        _parameters = {}
        for name, obj in self.get_objects(module_or_path).items():
            if parameters_filter(name, obj):
                _parameters.update({name: obj})

        return _parameters
