"""Extendable Module."""

import inspect


class Extendable:
    """Add the ability to extend classes on the fly."""

    def extend(self, key, obj=None):
        """Extend the current class with an object.

        This essentially extends a class on the fly.

        Arguments:
            key {string} -- The name of the method you want to set

        Keyword Arguments:
            obj {object} -- Any function, method or class (default: {None})

        Returns:
            self
        """
        # If both key and an object is passed
        if obj:
            if inspect.ismethod(obj):
                obj = obj.__func__

            setattr(self, key, obj.__get__(self))
            return self

        # Extend all of a classes methods into this class
        if inspect.isclass(key):
            for method in inspect.getmembers(key, inspect.isfunction):
                setattr(self, method[0], method[1].__get__(self))

        # Extend a function into this class
        elif inspect.isfunction(key):
            setattr(self, key.__name__, key.__get__(self))
        elif inspect.ismethod(obj):
            setattr(self, key.__name__, key.__func__.__get__(self))
        return self
