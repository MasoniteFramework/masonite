class PresetsCapsule:
    def __init__(self):
        self.presets = {}

    def add(self, preset):
        self.presets.update({preset.key: preset})
        return self

    def get_presets(self):
        return self.presets.values()

    def get_presets_keys(self):
        return self.presets.keys()

    def run(self, key):
        return self.presets.get(key).install()
