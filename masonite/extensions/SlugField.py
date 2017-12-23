from peewee import CharField
from slugify import slugify

class SlugField(CharField):

    def db_value(self, value):
        return slugify(value)

    def python_value(self, value):
        return value
