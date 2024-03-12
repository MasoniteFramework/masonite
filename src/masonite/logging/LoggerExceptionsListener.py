from ..facades import Log


class LoggerExceptionsListener:
    def handle(self, exception_type: str, exception: Exception):
        Log.error(f"{exception_type}: {exception}")
