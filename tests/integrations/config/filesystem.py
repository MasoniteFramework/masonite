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
    "openstack": {
        "driver": "openstack",
        "auth_url": os.getenv("OPENSTACK_AUTH_URL"),
        "project_name": os.getenv("OPENSTACK_PROJECT_NAME"),
        "username": os.getenv("OPENSTACK_USERNAME"),
        "password": os.getenv("OPENSTACK_PASSWORD"),
        "region": os.getenv("OPENSTACK_REGION"),
        "user_domain": os.getenv("OPENSTACK_USER_DOMAIN"),
        "project_domain": os.getenv("OPENSTACK_PROJECT_DOMAIN"),
        "app_name": os.getenv("OPENSTACK_APP_NAME"),
        "app_version": os.getenv("OPENSTACK_APP_VERSION"),
        "container": os.getenv("OPENSTACK_CONTAINER"),
    },
}
