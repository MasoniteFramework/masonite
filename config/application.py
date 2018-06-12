import os
from masonite.providers import (
    AppProvider,
    SessionProvider,
    CsrfProvider,
    RouteProvider,
    StatusCodeProvider,
    StartResponseProvider,
    SassProvider,
    WhitenoiseProvider,
    MailProvider,
    ViewProvider,
    HelpersProvider,
    UploadProvider,
    BroadcastProvider,
    CacheProvider
)

KEY = 'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='

BASE_DIRECTORY = os.getcwd()

URL = 'http://localhost'

PROVIDERS = [
    # Framework Providers
    AppProvider,
    SessionProvider,
    CsrfProvider,
    RouteProvider,
    StatusCodeProvider,
    StartResponseProvider,
    SassProvider,
    WhitenoiseProvider,
    MailProvider,
    ViewProvider,
    HelpersProvider,
    UploadProvider,
    BroadcastProvider,
    CacheProvider,
]

STATIC_ROOT = 'storage'

AUTOLOAD = []
