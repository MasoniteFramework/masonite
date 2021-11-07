from ..exceptions import AmbiguousError
import inspect


class Compact:
    def __new__(cls, *args):
        frame = inspect.currentframe()

        cls.dictionary = {}
        for arg in args:
            if isinstance(arg, dict):
                cls.dictionary.update(arg)
                continue

            found = []
            for key, value in frame.f_back.f_locals.items():
                if value == arg:
                    for f in found:
                        if value is f and f is not None:
                            raise AmbiguousError(
                                "Cannot contain variables with multiple of the same object in scope. "
                                "Getting {}".format(value)
                            )
                    cls.dictionary.update({key: value})
                    found.append(value)

        if len(args) != len(cls.dictionary):
            raise ValueError("Could not find all variables in this")
        return cls.dictionary
