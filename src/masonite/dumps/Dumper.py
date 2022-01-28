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

    def die_and_dump(self, *objects):
        """Dump all provided args and die, ie raise a DumpException."""
        self.dump(*objects)
        raise DumpException()

    def dump(self, *objects):
        """Dump all provided args and let flow continue. This does not raise a DumpException."""
        # get origin of dumped objects
        function, filename, line = (
            inspect.stack()[1].function,
            inspect.stack()[1].filename,
            inspect.stack()[1].lineno,
        )

        # get name of dumped objects
        some = inspect.currentframe().f_back.f_locals
        names = {}
        for name, var in some.items():
            names.update({str(var): name})
        named_objects = {}
        for obj in objects:
            name = names.get(str(obj), str(type(obj)))
            named_objects.update({name: obj})

        dump = Dump(
            named_objects,
            function,
            filename,
            line,
        )
        self.dumps.append(dump)
        return self.dumps

    def get_dumps(self, ascending=False):
        if ascending:
            return self.dumps
        else:
            new_dumps = self.dumps.copy()
            new_dumps.reverse()
            return new_dumps

    def get_serialized_dumps(self, ascending=False):
        return list(
            map(lambda dump: dump.serialize(), self.get_dumps(ascending=ascending))
        )
