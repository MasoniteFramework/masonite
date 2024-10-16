from ..facades import Session


def old(key: str, default: str = "") -> str:
    """Helper used to get value from session for the given key, with a default option."""
    return Session.get(key) or default
