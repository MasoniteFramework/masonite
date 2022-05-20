from typing import List, Tuple
from inflection import titleize

from .Header import Header


class HeaderBag:
    """Header bag used to manage HTTP Headers in the request and response."""

    def __init__(self):
        self.bag: dict = {}

    def add(self, header: "Header") -> None:
        """Add given header to the bag. If a header with the same name is already present, it will
        be overriden."""
        self.bag.update({self.convert_name(header.name): header})

    def add_if_not_exists(self, header: "Header") -> None:
        """Add given header to the bag if not present yet."""
        if self.convert_name(header.name) in self.bag:
            return None

        self.bag.update({self.convert_name(header.name): header})

    def get(self, name: str) -> "Header":
        """Get the header with the given name from the bag."""
        return self.bag.get(self.convert_name(name), "")

    def render(self) -> List[Tuple[str, str]]:
        """Render the header bag a list of tuple representing each headers. This will be used to
        be inserted in the WSGI response."""
        response = []
        for name, header in self.bag.items():
            response.append((name, header.value))

        return response

    def __contains__(self, name: str) -> bool:
        """Allow to use container comparison with header bag such as 'in'."""
        return self.convert_name(name) in self.bag.keys()

    def convert_name(self, name: str) -> str:
        """Convert uppercase and underscore HTTP header name to header title with dashes.

        HTTP_CUSTOM_VALUE will be converted to Custom-Value.
        X_RATE_LIMITED will be converted to X-Rate-Limited.
        """
        return titleize(name.replace("HTTP_", "")).replace(" ", "-")

    def load(self, environ: dict) -> None:
        """Load HTTP headers from WSGI dictionary into the bag (starting with HTTP_)."""
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                self.add(Header(key, value))

    def to_dict(self) -> dict:
        """Render the bag as a dictionary containing all headers."""
        dic = {}
        for name, header in self.bag.items():
            dic.update({name: header.value})

        return dic

    def __getitem__(self, key: str) -> "Header":
        """Allow to use python subscripting with header bag such as bag['HTTP_COOKIE']."""
        return self.bag[self.convert_name(key)]
