import inspect

from ..exceptions import DumpException
from .Dump import Dump


class Dumper:
    def __init__(self, application):
        self.app = application
        self.dumps = []

    def clear(self):
        """Clear all dumped data"""
        self.dumps = []
        return self

    def dd(self, *objects):
        """Dump all provided args and die, raising a DumpException."""
        self._dump(*objects)
        raise DumpException()

    def dump(self, *objects):
        """Dump all provided args and continue code execution. This does not raise a DumpException."""
        return self._dump(*objects)

    def get_dumps(self, ascending=False):
        """Get all dumps as Dump objects."""
        if ascending:
            return self.dumps
        else:
            new_dumps = self.dumps.copy()
            new_dumps.reverse()
            return new_dumps

    def last(self):
        """Return last added dump."""
        return self.dumps[-1]

    def get_serialized_dumps(self, ascending=False):
        """Get all dumps as dict."""
        return list(
            map(lambda dump: dump.serialize(), self.get_dumps(ascending=ascending))
        )

    def _dump(self, *objects):
        # get origin of dumped objects (go up 2 frames)
        function, filename, line = (
            inspect.stack()[2].function,
            inspect.stack()[2].filename,
            inspect.stack()[2].lineno,
        )

        # get name of dumped objects (go up 2 frames)
        some = inspect.currentframe().f_back.f_back.f_locals
        names = {}
        for name, var in some.items():
            names.update({str(var): name})
        named_objects = {}
        for obj in objects:
            # for variables dumped without name, use their type
            default = (
                f"<class '{obj.__name__}'>" if inspect.isclass(obj) else str(type(obj))
            )
            name = names.get(str(obj), default)
            named_objects.update({name: obj})

        dump = Dump(
            named_objects,
            function,
            filename,
            line,
        )
        self.dumps.append(dump)
        return self.dumps
