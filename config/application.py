import os

KEY='NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='

BASE_DIRECTORY = os.getcwd()

URL = 'http://localhost'

PROVIDERS = [
    # Framework Providers
    'masonite.providers.AppProvider.AppProvider',
    'masonite.providers.CsrfProvider.CsrfProvider',
    'masonite.providers.RouteProvider.RouteProvider',
    'masonite.providers.ApiProvider.ApiProvider',
    'masonite.providers.RedirectionProvider.RedirectionProvider',
    'masonite.providers.StartResponseProvider.StartResponseProvider',
    'masonite.providers.SassProvider.SassProvider',
    'masonite.providers.WhitenoiseProvider.WhitenoiseProvider',
    'masonite.providers.MailProvider.MailProvider',
    'masonite.providers.ViewProvider.ViewProvider',
    'masonite.providers.HelpersProvider.HelpersProvider',
    'masonite.providers.UploadProvider.UploadProvider',
    'masonite.providers.BroadcastProvider.BroadcastProvider',
    'masonite.providers.CacheProvider.CacheProvider',
]

STATIC_ROOT = 'storage'
