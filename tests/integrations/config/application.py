from src.masonite.environment import env

KEY = env("APP_KEY", "-RkDOqXojJIlsF_I8wWiUq_KRZ0PtGWTOZ676u5HtLg=")

DEBUG = env("APP_DEBUG", True)

HASHING = {
    "default": "bcrypt",
    "bcrypt": {"rounds": 10},
    "argon2": {"memory": 1024, "threads": 2, "time": 2},
}

APP_URL = env("APP_URL", "http://localhost:8000/")

MIX_BASE_URL = env("MIX_BASE_URL", None)
