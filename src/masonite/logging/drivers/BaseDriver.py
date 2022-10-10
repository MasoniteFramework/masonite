import pendulum


class BaseDriver:
    def __init__(self, application, name, options={}):
        self.application = application
        self.options = options
        self.name = name
        self.logger = self.application.make("logger")
        self.levels = self.logger.levels

        # for drivers which are using Python logging module
        self.logging_logger = None
        self.logging_handler = None

    def set_options(self, options):
        self.options = options
        return self

    def get_min_level(self):
        return self.levels.get(
            self.options.get("level", self.logger.get_default_level())
        )

    def get_format(self):
        return self.options.get("format", self.logger.get_default_format())

    def should_send(self, level):
        return self.get_min_level() <= self.levels.get(level)

    def get_time(self):
        return pendulum.now().in_tz(
            self.options.get("timezone", self.logger.get_default_timezone())
        )

    def get_formatted_time(self):
        date_format = self.options.get(
            "date_format", self.logger.get_default_date_format()
        )
        return self.get_time().format(date_format)

    def set_logger(self):
        for handler in self.logging_logger.handlers:
            self.logging_logger.removeHandler(handler)
        self.logging_logger.addHandler(self.logging_handler)
        self.logging_logger.setLevel(self.get_min_level())

    def format_message(self, message, level, timestamp):
        log_format = self.get_format()
        # Formatter().format(formatter, )
        # TODO:

        return message

    def send(self, level, message):
        # if not self.should_send(level):
        #     return False

        # timestamp = self.get_time()
        # formatted_message = self.format_message(message, level, timestamp)
        # return {
        #     "formatted_message": formatted_message,
        #     "level": level,
        #     "message": message,
        #     "timestamp": timestamp,
        # }
        raise NotImplementedError()

    def log(self, level, message):
        return self.send(self.levels.get(level), message)

    def debug(self, message):
        return self.send(self.levels.get("debug"), message)

    def info(self, message):
        return self.send(self.levels.get("info"), message)

    def notice(self, message):
        return self.send(self.levels.get("notice"), message)

    def warning(self, message):
        return self.send(self.levels.get("warning"), message)

    def error(self, message):
        return self.send(self.levels.get("error"), message)

    def critical(self, message):
        return self.send(self.levels.get("critical"), message)

    def alert(self, message):
        return self.send(self.levels.get("alert"), message)

    def emergency(self, message):
        return self.send(self.levels.get("emergency"), message)
