"""Cache Config"""
import os
from src.masonite.utils.location import base_path

DISKS = {
    "default": "local",
    "local": {
        "driver": "file",
        "path": base_path("storage/framework/filesystem"),
    },
    "s3": {
        "driver": "s3",
        "client": os.getenv("AWS_CLIENT"),
        "secret": os.getenv("AWS_SECRET"),
        "bucket": os.getenv("AWS_BUCKET"),
    },
}
