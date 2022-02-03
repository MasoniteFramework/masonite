class DriverNotFound(Exception):
    pass


class DriverLibraryNotFound(Exception):
    pass


class FileTypeException(Exception):
    pass


class RequiredContainerBindingNotFound(Exception):
    pass


class MissingContainerBindingNotFound(Exception):
    pass


class UnacceptableDriverType(Exception):
    pass


class ContainerError(Exception):
    pass


class InvalidCSRFToken(Exception):
    pass


class InvalidHTTPStatusCode(Exception):
    pass


class RouteMiddlewareNotFound(Exception):
    pass


class ResponseError(Exception):
    pass


class InvalidAutoloadPath(Exception):
    pass


class AutoloadContainerOverwrite(Exception):
    pass


class InvalidSecretKey(Exception):
    pass


class InvalidToken(Exception):
    pass


class StrictContainerException(Exception):
    pass


class InvalidRouteCompileException(Exception):
    pass


class RouteException(Exception):
    pass


class RouteNotFoundException(Exception):
    is_http_exception = True

    def __init__(self, message):
        super().__init__(message)
        self.message = message or "Route Not Found"

    def get_response(self):
        return self.message

    def get_status(self):
        return 404


class DebugException(Exception):
    pass


class DumpException(Exception):
    pass


class ViewException(Exception):
    pass


class QueueException(Exception):
    pass


class AmbiguousError(Exception):
    pass


class ProjectLimitReached(Exception):
    pass


class ProjectProviderTimeout(Exception):
    pass


class ProjectProviderHttpError(Exception):
    pass


class ProjectTargetNotEmpty(Exception):
    pass


class NotificationException(Exception):
    pass


class AuthorizationException(Exception):
    is_http_exception = True

    def __init__(self, message="", status=403):
        super().__init__(message)
        self.message = message or "Action not authorized"
        self.status = status or 403

    def get_response(self):
        return self.message

    def get_status(self):
        return self.status


class GateDoesNotExist(Exception):
    pass


class PolicyDoesNotExist(Exception):
    pass


class MixManifestNotFound(Exception):
    pass


class MixFileNotFound(Exception):
    pass


class InvalidConfigurationLocation(Exception):
    pass


class InvalidConfigurationSetup(Exception):
    pass


class InvalidPackageName(Exception):
    pass


class LoaderNotFound(Exception):
    pass
