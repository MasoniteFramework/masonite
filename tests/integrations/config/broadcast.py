"""Cache Config"""

import os

BROADCASTS = {
    "default": "pusher",
    "pusher": {
        "driver": "pusher",
        "client": os.getenv("PUSHER_CLIENT"),
        "app_id": os.getenv("PUSHER_APP_ID"),
        "secret": os.getenv("PUSHER_SECRET"),
        "cluster": os.getenv("PUSHER_CLUSTER"),
        "ssl": False,
    },
}
