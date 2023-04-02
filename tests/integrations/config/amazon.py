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
