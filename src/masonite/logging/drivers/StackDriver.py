from .BaseDriver import BaseDriver


class StackDriver(BaseDriver):
    def __init__(self, application, name, options):
        super().__init__(application, name, options)

    def send(self, level, message):
        logger = self.application.make("logger")
        level_name = logger.get_level_name(level)
        for channel in self.options.get("channels", []):
            logger.channel(channel).log(level_name, message)
