from .Provider import Provider
from whitenoise import WhiteNoise
import os


class WhitenoiseProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):

        response_handler = WhiteNoise(
            self.application.get_response_handler(),
            root=self.application.get_storage_path(),
            autorefresh=True,
        )

        for location, alias in (
            self.application.make("storage_capsule").get_storage_assets().items()
        ):
            response_handler.add_files(location, prefix=alias)

        self.application.set_response_handler(response_handler)

    def boot(self):
        return
