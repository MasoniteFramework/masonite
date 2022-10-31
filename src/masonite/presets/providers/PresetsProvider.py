from ...providers import Provider
from ..PresetsCapsule import PresetsCapsule
from .. import Tailwind, Vue, React, Bootstrap


class PresetsProvider(Provider):
    """Manage frontend presets."""

    def __init__(self, app):
        self.application = app

    def register(self):
        presets = PresetsCapsule()
        presets.add(Bootstrap())
        presets.add(Tailwind())
        presets.add(Vue())
        presets.add(React())
        self.application.bind("presets", presets)

    def boot(self):
        pass
