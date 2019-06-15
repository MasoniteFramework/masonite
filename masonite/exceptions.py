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


class StrictContainerException(Exception):
    pass


class InvalidRouteCompileException(Exception):
    pass


class RouteException(Exception):
    pass


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
