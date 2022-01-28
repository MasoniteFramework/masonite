import inspect
import json


def is_property(obj):
    return not inspect.ismethod(obj)


def is_local(obj_name, obj):
    return (
        not obj_name.startswith("__")
        and not obj_name.endswith("__")
        and not type(obj).__name__ == "builtin_function_or_method"
    )


def serialize_property(obj):
    if isinstance(obj, list):
        local_list = []
        for subobj in obj:
            local_list.append(serialize_property(subobj))
        return local_list
    elif isinstance(obj, dict):
        local_dict = {}
        for key, val in obj.items():
            local_dict.update({key: serialize_property(val)})
        return local_dict
    elif hasattr(obj, "serialize"):
        return obj.serialize()
    else:
        return str(obj)


class DumpExceptionHandler:
    def __init__(self, application):
        self.application = application

    def handle(self, exception):
        dump_objs = []
        for dump in self.application.make("dumper").get_dumps():
            for obj_name, obj in dump.objects.items():
                all_members = inspect.getmembers(obj, predicate=inspect.ismethod)
                all_properties = inspect.getmembers(obj, predicate=is_property)
                members = {
                    name: str(member)
                    for name, member in all_members
                    if is_local(name, member)
                }
                properties = {
                    name: serialize_property(prop)
                    for name, prop in all_properties
                    if is_local(name, prop)
                }
                dump_objs.append(
                    {
                        "name": obj_name,
                        "obj": str(obj),
                        "members": members,
                        "properties": properties,
                    }
                )
        self.application.make("view").add_extension(
            "jinja2_highlight.HighlightExtension"
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
