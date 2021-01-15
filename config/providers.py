"""Providers Configuration File."""

from src.masonite.providers import (AppProvider, AuthenticationProvider, BroadcastProvider, CacheProvider,
                                CsrfProvider, HelpersProvider, MailProvider,
                                QueueProvider, RouteProvider,
                                SessionProvider, StatusCodeProvider,
                                UploadProvider, ViewProvider,
                                WhitenoiseProvider)

from masoniteorm.providers.ORMProvider import ORMProvider

"""Providers List
Providers are a simple way to remove or add functionality for Masonite
The providers in this list are either ran on server start or when a
request is made depending on the provider. Take some time to can
learn more more about Service Providers in our documentation
"""

PROVIDERS = [
    # Framework Providers
    AppProvider,
    CsrfProvider,
    SessionProvider,
    RouteProvider,
    StatusCodeProvider,
    WhitenoiseProvider,
    ViewProvider,
    AuthenticationProvider,
    ORMProvider,

    # Optional Framework Providers
    MailProvider,
    UploadProvider,
    QueueProvider,
    CacheProvider,
    BroadcastProvider,
    CacheProvider,
    HelpersProvider,

    # Third Party Providers

    # Application Providers

]
