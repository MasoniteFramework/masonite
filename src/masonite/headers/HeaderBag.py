from typing import List, Dict

from .Header import Header
from inflection import titleize


class HeaderBag:
    def __init__(self):
        self.bag = {}

    def add(self, header) -> None:
        self.bag.update({self.convert_name(header.name): header})

    def add_if_not_exists(self, header) -> None:
        if self.convert_name(header.name) in self.bag:
            return None

        self.bag.update({self.convert_name(header.name): header})

    def get(self, name):
        return self.bag.get(self.convert_name(name), "")

    def render(self) -> List:
        response = []
        for name, header in self.bag.items():
            response.append((name, header.value))

        return response

    def __contains__(self, name):
        return self.convert_name(name) in self.bag.keys()

    def convert_name(self, name) -> str:
        return titleize(name.replace("HTTP_", "")).replace(" ", "-")

    def load(self, environ) -> None:
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                self.add(Header(key, value))

    def to_dict(self) -> Dict:
        dic = {}
        for name, header in self.bag.items():
            dic.update({name: header.value})

        return dic

    def __getitem__(self, key):
        return self.bag[self.convert_name(key)]
