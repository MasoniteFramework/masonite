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
from events.providers import EventProvider

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
    EventProvider,
]
