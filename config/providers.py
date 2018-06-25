""" Providers Configuration File """

from masonite.providers import (
    AppProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    StartResponseProvider,
    SassProvider,
    WhitenoiseProvider,
    MailProvider,
    UploadProvider,
    ViewProvider,
    HelpersProvider,
    QueueProvider,
    BroadcastProvider,
    CacheProvider,
    CsrfProvider,
)

from app.providers.MiddlewareProvider import MiddlewareProvider
from app.providers.UserModelProvider import UserModelProvider

'''
|--------------------------------------------------------------------------
| Providers List
|--------------------------------------------------------------------------
|
| Providers are a simple way to remove or add functionality for Masonite
| The providers in this list are either ran on server start or when a
| request is made depending on the provider. Take some time to can
| learn more more about Service Providers in our documentation
|
'''


PROVIDERS = [
    # Framework Providers
    AppProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    StartResponseProvider,
    WhitenoiseProvider,
    ViewProvider,

    # Optional Framework Providers
    SassProvider,
    MailProvider,
    UploadProvider,
    QueueProvider,
    CacheProvider,
    BroadcastProvider,
    CacheProvider,
    CsrfProvider,
    HelpersProvider,

    # Third Party Providers

    # Application Providers
    UserModelProvider,
    MiddlewareProvider,
]
