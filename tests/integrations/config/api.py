from ..app.User import User

DRIVERS = {
    "jwt": {
        "algorithm": "HS512",
        "secret": "secret",
        "model": User,
        "expires": None,
        "authenticates": False,
        "version": None,
    }
}
