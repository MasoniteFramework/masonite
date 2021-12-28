from .Input import Input
from urllib.parse import parse_qs
import re
import json
import cgi
import re
from ..utils.structures import data_get
from ..filesystem import UploadedFile


class InputBag:
    def __init__(self):
        self.query_string = {}
        self.post_data = {}
        self.environ = {}

    def load(self, environ):
        self.environ = environ
        self.query_string = {}
        self.post_data = {}
        self.parse(environ)
        return self

    def parse(self, environ):
        if "QUERY_STRING" in environ:
            self.query_string = self.query_parse(environ["QUERY_STRING"])

        if "wsgi.input" in environ:
            if "application/json" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)

                if isinstance(request_body, bytes):
                    request_body = request_body.decode("utf-8")

                json_payload = json.loads(request_body or "{}")
                if isinstance(json_payload, list):
                    pass
                else:
                    for name, value in json.loads(request_body or "{}").items():
                        self.post_data.update({name: Input(name, value)})

            elif "application/x-www-form-urlencoded" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)
                parsed_request_body = parse_qs(bytes(request_body).decode("utf-8"))

                self.post_data = self.parse_dict(parsed_request_body)

            elif "multipart/form-data" in environ.get("CONTENT_TYPE", ""):
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                fields = cgi.FieldStorage(
                    fp=environ["wsgi.input"],
                    environ=environ,
                    keep_blank_values=1,
                )

                for name in fields:
                    value = fields.getvalue(name)
                    if isinstance(value, bytes):
                        self.post_data.update(
                            {name: UploadedFile(fields[name].filename, value)}
                        )
                    else:
                        self.post_data.update({name: Input(name, value)})

                self.post_data = self.parse_dict(self.post_data)
            else:
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)
                if request_body:
                    self.post_data.update(
                        json.loads(bytes(request_body).decode("utf-8"))
                    )

    def get(self, name, default=None, clean=True, quote=True):
        input = data_get(self.all(), name, default)

        if isinstance(input, (str,)):
            return input
        if isinstance(input, list) and len(input) == 1:
            return input[0]
        elif isinstance(input, (dict,)):
            rendered = {}
            for key, inp in input.items():
                if hasattr(inp, "value"):
                    inp = inp.value
                rendered.update({key: inp})
            return rendered
        elif hasattr(input, "value"):
            if isinstance(input.value, list) and len(input.value) == 1:
                return input.value[0]
            elif isinstance(input.value, dict):
                return input.value
            return input.value

        return input

    def has(self, *names):
        return all((name in self.all()) for name in names)

    def all(self):
        all = {}
        qs = self.query_string
        if isinstance(qs, list):
            qs = {str(i): v for i, v in enumerate(qs)}

        all.update(qs)
        all.update(self.post_data)
        return all

    def all_as_values(self, internal_variables=False):
        all = self.all()
        new = {}
        for name, input in all.items():
            if not internal_variables:
                if name.startswith("__"):
                    continue
            new.update({name: self.get(name)})

        return new

    def only(self, *args):
        all = self.all()
        new = {}
        for name, input in all.items():
            if name not in args:
                continue
            new.update({name: self.get(name)})

        return new

    def query_parse(self, query_string):
        return self.parse_dict(parse_qs(query_string))

    def parse_dict(self, dictionary):
        d = {}
        for name, value in dictionary.items():
            if name.endswith("[]"):
                d.update({name: value})
            else:
                regex_match = re.match(r"(?P<name>[^\[]+)\[(?P<value>[^\]]+)\]", name)

                if regex_match:
                    gd = regex_match.groupdict()
                    if isinstance(value, Input):
                        d.setdefault(gd["name"], {})[gd["value"]] = value
                    else:
                        d.setdefault(gd["name"], {})[gd["value"]] = value[0]
                else:
                    try:
                        d.update({name: value[0]})
                    except TypeError:
                        d.update({name: value})

        new_dict = {}
        # Further filter the dictionary
        for name, value in d.items():
            if "[]" in name:
                new_name = name.replace("[]", "")
                regex_match = re.match(
                    r"(?P<name>[^\[]+)*\[(?P<value>[^\]]+)\]", new_name
                )
                if regex_match:
                    new_dict.setdefault(regex_match["name"], []).append(
                        {regex_match["value"]: value}
                    )
                else:
                    new_dict.update({name: value})
            else:
                new_dict.update({name: value})

        return new_dict

    def add_post(self, key, value):
        self.post_data.update({key: value})
        return value
