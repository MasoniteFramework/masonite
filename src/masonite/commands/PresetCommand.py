"""New Preset Command."""

from .Command import Command
from ..presets import Tailwind, Vue, React, Bootstrap, Remove


class PresetCommand(Command):
    """
    Scaffold frontend preset in your project

    preset
        {name? : Name of the preset [tailwind, vue, react, bootstrap]}
        {--r|remove=? : Remove all scaffolded presets}
    """

    presets = ["vue", "tailwind", "react", "bootstrap"]

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        preset_name = self.argument("name")
        remove_presets = self.option("remove")
        if remove_presets:
            return self.remove()

        if preset_name not in self.presets:
            return self.error(
                f"Invalid preset. Available presets are: {', '.join(self.presets)}"
            )

        self.info(f"Scaffolding {preset_name} preset...")
        return getattr(self, preset_name)()

    def remove(self):
        Remove().install()
        self.info("Frontend scaffolding removed successfully.")

    def react(self):
        React().install()
        self.info("React installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def vue(self):
        Vue().install()
        self.info("Vue 3.0 installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
        self.comment("Then you can use the view app_vue3 as demo.")

    def bootstrap(self):
        Bootstrap().install()
        self.info("Bootstrap installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def tailwind(self):
        Tailwind().install()
        self.info("TailwindCSS 3 installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
