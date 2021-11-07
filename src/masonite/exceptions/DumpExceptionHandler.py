import inspect


class DumpExceptionHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        dump_objs = []
        for dump_name in self.application.make("ObjDumpList"):
            obj = self.application.make(dump_name)
            dump_objs.append(
                {
                    "obj": obj,
                    "members": inspect.getmembers(obj, predicate=inspect.ismethod),
                    "properties": inspect.getmembers(obj),
                }
            )

        return self.application.make("response").view(
            self.application.make("view").render(
                "/masonite/templates/dump",
                {
                    "objs": dump_objs,
                    "type": type,
                    "list": list,
                    "inspect": inspect,
                    "hasattr": hasattr,
                    "getattr": getattr,
                    "isinstance": isinstance,
                    "show_methods": (bool, str, list, dict),
                    "len": len,
                },
            )
        )
