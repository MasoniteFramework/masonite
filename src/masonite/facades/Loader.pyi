from typing import Any

class Loader:
    def get_modules(files_or_directories: list, raise_exception: bool = False) -> dict:
        """Get a list of Python modules found (recursively) in the given list of files or directories.
        If raise_exception is enabled it will raise an exception in case of error during loading a module."""
    def find(
        class_instance: Any,
        paths: list,
        class_name: str,
        raise_exception: bool = False,
    ) -> "None|Any": ...
    def find_all(
        class_instance: Any, paths: list, raise_exception: bool = False
    ) -> dict: ...
    def get_object(
        path_or_module: "str|Any", object_name: str, raise_exception: bool = False
    ) -> Any:
        """Load the given object from a Python module located at path and returns a default value if
        not found. If no object name is provided, returns the loaded module."""
        ...
    def get_objects(
        path_or_module: "str|Any",
        filter_method: callable = None,
        raise_exception: bool = False,
    ) -> dict:
        """Returns a dictionary of objects from the given path (file or dotted). The dictionary can
        be filtered if a given callable is given."""
        ...
    def get_parameters(module_or_path: "str|Any") -> dict: ...
