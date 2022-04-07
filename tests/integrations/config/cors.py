"""Cross-Origin Resource Sharing (CORS) config"""

PATHS = ["api/*", "sanctum/csrf-cookie", "server1.com"]

ALLOWED_METHODS = ["*"]

ALLOWED_ORIGINS = ["*"]

ALLOWED_HEADERS = ["*"]

EXPOSED_HEADERS = []

MAX_AGE = None

SUPPORTS_CREDENTIALS = False
