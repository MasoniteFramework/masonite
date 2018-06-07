import os

KEY = 'NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='

BASE_DIRECTORY = os.getcwd()

URL = 'http://localhost'

PROVIDERS = [
    # Framework Providers
    'masonite.providers.AppProvider',
    'masonite.providers.SessionProvider',
    'masonite.providers.CsrfProvider',
    'masonite.providers.RouteProvider',
    'masonite.providers.StatusCodeProvider',
    'masonite.providers.StartResponseProvider',
    'masonite.providers.SassProvider',
    'masonite.providers.WhitenoiseProvider',
    'masonite.providers.MailProvider',
    'masonite.providers.ViewProvider',
    'masonite.providers.HelpersProvider',
    'masonite.providers.UploadProvider',
    'masonite.providers.BroadcastProvider',
    'masonite.providers.CacheProvider',
]

STATIC_ROOT = 'storage'

AUTOLOAD = []
