from .Input import Input
from urllib.parse import parse_qs
import email.parser
import json
import cgi
import re
from ..helpers import Dot as DictDot, clean_request_input


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
                if isinstance(request_body, bytes):
                    request_body = request_body.decode("utf-8")

                for parts in request_body.split("&"):
                    name, value = parts.split("=", 1)
                    self.post_data.update({name: Input(name, value)})
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
                    self.post_data.update({name: Input(name, fields.getvalue(name))})
            else:
                try:
                    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                except (ValueError):
                    request_body_size = 0

                request_body = environ["wsgi.input"].read(request_body_size)

    def get(self, name, default=None):

        input = DictDot().dot(name, self.all(), default=default)
        if isinstance(input, (dict, str)):
            return input
        elif hasattr(input, "value"):
            return input.value
        else:
            return input

        return default

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

    def query_parse(self, query_string):
        d = {}
        for name, value in parse_qs(query_string).items():
            regex_match = re.match(r"(?P<name>[^\[]+)\[(?P<value>[^\]]+)\]", name)
            if regex_match:
                gd = regex_match.groupdict()
                d.setdefault(gd["name"], {})[gd["value"]] = Input(name, value[0])
            else:
                d.update({name: Input(name, value[0])})

        return d
