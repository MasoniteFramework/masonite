"""User Model."""

from masonite.orm.models import Model


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
