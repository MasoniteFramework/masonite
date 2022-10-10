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
        "path": "logs/single.log",
    },
    "daily": {
        "driver": "daily",
        "path": "logs/daily.log",
        "days": 7,
        "keep": 10,
    },
    "all": {"driver": "stack", "channels": ["single", "daily", "console"]},
    # "syslog": {
    #     "driver": "syslog",
    #     # ...syslog options
    # },
    # "slack": {
    #     "driver": "slack",
    #     # ...slack options
    # },
    # "papertrail": {"driver": "syslog", "host": "", "port": ""},
}
