from .Header import Header
from inflection import humanize, dasherize, camelize, titleize


class HeaderBag:
    def __init__(self):
        self.bag = {}

    def add(self, header):
        self.bag.update({self.convert_name(header.name): header})

    def add_if_not_exists(self, header):
        if self.convert_name(header.name) in self.bag:
            return None

        self.bag.update({self.convert_name(header.name): header})

    def get(self, name):
        return self.bag.get(self.convert_name(name), "")

    def render(self):
        response = []
        for name, header in self.bag.items():
            response.append((name, header.value))

        return response

    def __contains__(self, name):
        return self.convert_name(name) in self.bag.keys()

    def convert_name(self, name):
        return titleize(name.replace("HTTP_", "")).replace(" ", "-")

    def load(self, environ):
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                self.add(Header(key, value))

    def to_dict(self):
        dic = {}
        for name, header in self.bag.items():
            dic.update({name: header.value})

        return dic

    def __getitem__(self, key):
        return self.bag[self.convert_name(key)]
