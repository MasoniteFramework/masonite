from ..facades import Session


def old(key: str) -> str:
    """Helper used to get value from session for the given key."""
    return Session.get(key) or ""
