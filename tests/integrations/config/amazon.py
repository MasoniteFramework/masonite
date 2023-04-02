import os

SERVICES = {
    "s3": {
        "buckets": {
            "images": "the-images",
            "console": "console-attachments",
        },
        "options": {
            "endpoint_url": "http://localhost:4566",
            "aws_access_key_id": os.getenv("AWS_CLIENT"),
            "aws_secret_access_key": os.getenv("AWS_SECRET"),
        },
    },
    # using a more readable alias for the service
    "api_gateway": {
        "service": "apigateway",
        "options": {
            "aws_access_key_id": os.getenv("AWS_CLIENT"),
            "aws_secret_access_key": os.getenv("AWS_SECRET"),
        },
    },
    "disabled": {
        "active": False,
        "service": "s3",
    },
    "invalid": {
        "active": True,
        "service": "dummy",
        "options": {
            "aws_access_key_id": os.getenv("AWS_CLIENT"),
            "aws_secret_access_key": os.getenv("AWS_SECRET"),
        },

    },
}
