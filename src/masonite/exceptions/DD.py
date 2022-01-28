import inspect
import warnings

from .exceptions import DumpException


warnings.warn(
    "DD class will be removed in Masonite 5. Please use Dump facade instead.",
    DeprecationWarning,
)


class DD:
    def __init__(self, container):
        self.app = container

    def die_and_dump(self, *args):
        """Dump all provided args and die, ie raise a DumpException."""
        self.dump(*args)
        raise DumpException

    def dump(self, *args):
        """Dump all provided args and let flow continue. This does not raise a DumpException."""
        print(
            inspect.stack()[1].function,
            inspect.stack()[1].filename,
            inspect.stack()[1].lineno,
        )
        if self.app.has("ObjDumpList"):
            dump_list = self.app.make("ObjDumpList")
        else:
            dump_list = []
        start = len(dump_list)
        for i, obj in enumerate(args):
            dump_name = f"ObjDump{start + i}"
            self.app.bind(dump_name, obj)
            dump_list.append(dump_name)
        self.app.bind("ObjDumpList", dump_list)
