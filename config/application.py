import os

KEY='NCTpkICMlTXie5te9nJniMj9aVbPM6lsjeq5iDZ0dqY='

BASE_DIRECTORY = os.getcwd()

PROVIDERS = [
    # Framework Providers
    'masonite.providers.AppProvider.AppProvider',
    'masonite.providers.RouteProvider.RouteProvider',
    'masonite.providers.ApiProvider.ApiProvider',
    'masonite.providers.RedirectionProvider.RedirectionProvider',
    'masonite.providers.StartResponseProvider.StartResponseProvider',
    'masonite.providers.SassProvider.SassProvider',
    'masonite.providers.WhitenoiseProvider.WhitenoiseProvider',
    'masonite.providers.MailProvider.MailProvider',
]

STATIC_ROOT = 'storage'
