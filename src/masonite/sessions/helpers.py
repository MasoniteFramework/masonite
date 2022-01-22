from ..facades import Session


def old(key):
    """"""
    return Session.get(key) or ""
