from ...providers import Provider
from ..PresetsCapsule import PresetsCapsule
from .. import Tailwind, Vue, React, Bootstrap


class PresetsProvider(Provider):
    """
    @M5
    This provider will be used in Masonite 5. For now, this code is added
    into the FrameworkProvider to allow projects without PresetsProvider to
    work."""

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
