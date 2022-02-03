"""New Preset Command."""
from .Command import Command
from ..presets import Remove


class PresetCommand(Command):
    """
    Scaffold frontend preset in your project

    preset
        {name? : Name of the preset}
        {--r|remove=? : Remove all scaffolded presets}
        {--l|list=? : List all available presets}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        preset_name = self.argument("name")
        remove_presets = self.option("remove")
        list_presets = self.option("list")

        presets = self.app.make("presets")
        available_presets = presets.get_presets_keys()

        if list_presets:
            return self.info(f"Available presets are: {', '.join(available_presets)}")

        if remove_presets:
            return self.remove()

        if preset_name not in available_presets:
            return self.error(
                f"Invalid preset. Available presets are: {', '.join(available_presets)}"
            )

        self.info(f"Scaffolding {preset_name} preset...")
        presets.run(preset_name)
        self.info(f"{preset_name} installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def remove(self):
        Remove().install()
        self.info("Frontend scaffolding removed successfully.")
