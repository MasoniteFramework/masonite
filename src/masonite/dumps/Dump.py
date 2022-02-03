import time
import inspect


def is_property(obj):
    return not inspect.ismethod(obj)


def is_local(obj_name, obj):
    return (
        not obj_name.startswith("__")
        and not obj_name.endswith("__")
        and not type(obj).__name__ == "builtin_function_or_method"
    )


def is_private(obj_name):
    return obj_name.startswith("_")


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


class Dump:
    def __init__(self, objects, method, filename, line):
        self.objects = objects
        self.method = method
        self.filename = filename
        self.line = line
        self.timestamp = time.time()

    def serialize(self):
        objects = {}
        for name, obj in self.objects.items():
            # serialize all obj properties
            all_properties = inspect.getmembers(obj, predicate=is_property)
            local_properties = {"private": {}, "public": {}}
            for prop_name, prop in all_properties:
                if is_local(prop_name, prop):
                    entry = {prop_name: serialize_property(prop)}
                    if is_private(prop_name):
                        local_properties["private"].update(entry)
                    else:
                        local_properties["public"].update(entry)

            objects.update({name: {"value": str(obj), "properties": local_properties}})

        return {
            "objects": objects,
            "method": self.method,
            "filename": self.filename,
            "line": self.line,
            "timestamp": self.timestamp,
        }

    def __repr__(self):
        return self._format()

    def __str__(self):
        return self._format()

    def _format(self):
        return f"""DUMP -> {self.filename}: {self.line} in {self.method}()
        {self.objects}
        """
