import os

# defined for testing purposes only
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", os.getenv("AWS_CLIENT"))
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET"))

SERVICES = {
    "s3": {
        "buckets": {
            "images": "the-images",
            "console": "console-attachments",
        },
        "options": {
            "endpoint_url": "http://localhost:4566",
        },
    },
    # using a more readable alias for the service
    "api_gateway": {
        "service": "apigateway",
    },
    "disabled": {
        "active": False,
        "service": "s3",
    },
    "invalid": {
        "active": True,
        "service": "dummy",
    },
}
