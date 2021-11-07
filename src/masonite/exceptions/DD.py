from .exceptions import DumpException


class DD:
    def __init__(self, container):
        self.app = container

    def dump(self, *args):
        dump_list = []
        for i, obj in enumerate(args):
            dump_name = "ObjDump{}".format(i)
            self.app.bind(dump_name, obj)
            dump_list.append(dump_name)
        self.app.bind("ObjDumpList", dump_list)
        raise DumpException
