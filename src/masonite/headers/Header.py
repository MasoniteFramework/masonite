class Header:
    """Class used to represent a HTTP header."""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
