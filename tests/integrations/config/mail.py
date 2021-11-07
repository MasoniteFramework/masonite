import os


DRIVERS = {
    "default": "smtp",
    "smtp": {
        "host": os.getenv("MAIL_HOST"),
        "port": os.getenv("MAIL_PORT"),
        "username": os.getenv("MAIL_USERNAME"),
        "password": os.getenv("MAIL_PASSWORD"),
    },
    "mailgun": {
        "domain": os.getenv("MAILGUN_DOMAIN"),
        "secret": os.getenv("MAILGUN_SECRET"),
    },
}
