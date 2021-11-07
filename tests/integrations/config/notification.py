"""Notifications Settings."""
import os

DRIVERS = {
    "slack": {
        "token": os.getenv("SLACK_TOKEN", ""),  # used for API mode
        "webhook": os.getenv("SLACK_WEBHOOK", ""),  # used for webhook mode
        # "mode": os.getenv("SLACK_MODE", "webhook"),  # webhook or api
    },
    "vonage": {
        "key": os.getenv("VONAGE_KEY", ""),
        "secret": os.getenv("VONAGE_SECRET", ""),
        "sms_from": os.getenv("VONAGE_SMS_FROM", "+33000000000"),
    },
    "database": {
        "connection": "sqlite",
        "table": "notifications",
    },
}

DRY = False
