from src.masonite.providers import (
    RouteProvider,
    FrameworkProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    SessionProvider,
    QueueProvider,
    CacheProvider,
    EventProvider,
    StorageProvider,
    HelpersProvider,
    BroadcastProvider,
    AuthenticationProvider,
    AuthorizationProvider,
    HashServiceProvider,
    ORMProvider,
)


from src.masonite.scheduling.providers import ScheduleProvider
from src.masonite.notification.providers import NotificationProvider
from src.masonite.validation.providers.ValidationProvider import ValidationProvider
from src.masonite.api.providers import ApiProvider
from ..test_package import MyTestPackageProvider

from tests.integrations.providers import AppProvider

PROVIDERS = [
    FrameworkProvider,
    HelpersProvider,
    RouteProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    NotificationProvider,
    SessionProvider,
    CacheProvider,
    QueueProvider,
    ScheduleProvider,
    EventProvider,
    StorageProvider,
    BroadcastProvider,
    HashServiceProvider,
    AuthenticationProvider,
    AuthorizationProvider,
    ValidationProvider,
    MyTestPackageProvider,
    AppProvider,
    ORMProvider,
    ApiProvider,
]
