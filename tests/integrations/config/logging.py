CHANNELS = {
    "default": {
        "driver": "console",
        "level": "info",
        "timezone": "UTC",
        "format": "{timestamp} - {levelname}: {message}",
        "date_format": "YYYY-MM-DD HH:mm:ss",
    },
    "console": {
        "driver": "terminal",
        # "format": "> {timestamp} - {levelname}: {message}",
        # "date_format": "YYYY-MM-DD HH:mm:ss",
    },
    "single": {
        "driver": "single",
        "path": "logs/masonite.log",
    },
    "daily": {
        "driver": "daily",
        "days": 7,
        "keep": 10,
    },
    "all": {"driver": "stack", "channels": ["single", "daily", "console"]},
    "syslog": {"driver": "syslog", "address": "/var/log/system.log"},
    "papertrail": {
        "driver": "syslog",
        "host": "logs.papertrailapp.com",
        "port": None,  # specify here the port as an integer
    },
    "slack": {
        "driver": "slack",
        "webhook_url": "",
    },
}
