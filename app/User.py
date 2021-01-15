"""User Model."""

from masoniteorm.models import Model


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
