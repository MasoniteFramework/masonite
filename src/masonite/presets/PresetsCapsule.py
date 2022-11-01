from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .Preset import Preset


class PresetsCapsule:
    """Presets capsule class used to manage Presets in the project."""

    def __init__(self):
        self.presets: dict = {}

    def add(self, preset: "Preset") -> "PresetsCapsule":
        self.presets.update({preset.key: preset})
        return self

    def get_presets(self) -> "List[Preset]":
        return self.presets.values()

    def get_presets_keys(self) -> list:
        """Get a list of available presets name."""
        return self.presets.keys()

    def run(self, key: str):
        """Apply the given preset name to the project."""
        return self.presets.get(key).install()
