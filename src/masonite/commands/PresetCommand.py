"""New Preset System Command."""
from cleo import Command
from ..commands.presets.React import React
from ..commands.presets.Vue import Vue
from ..commands.presets.Vue3 import Vue3
from ..commands.presets.Bootstrap import Bootstrap
from ..commands.presets.Remove import Remove
from ..commands.presets.Tailwind import Tailwind


class PresetCommand(Command):
    """
    Swap the front-end scaffolding for the application

    preset
        {name : Name of the preset}
    """

    def handle(self):
        self.info("Scaffolding Application ...")
        preset_name = self.argument("name")
        presets_list = ["react", "vue", "vue3", "remove", "bootstrap", "tailwind2"]
        if preset_name not in presets_list:
            raise ValueError("Invalid preset. Choices are: {0}".format(presets_list))
        return getattr(self, preset_name)()

    def remove(self):
        """Removes frontend scaffolding"""
        Remove().install()
        self.info("Frontend scaffolding removed successfully.")

    def react(self):
        """Add React frontend while also removing Vue (if it was previously selected)"""
        React().install()
        self.info("React scaffolding installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def vue(self):
        """Add Vue frontend while also removing React (if it was previously selected)"""
        Vue().install()
        self.info("Vue scaffolding installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def vue3(self):
        """Add Vue 3.0 frontend while also removing React (if it was previously selected)"""
        Vue3().install()
        self.info("Vue 3.0 scaffolding installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
        self.comment("Then you can use the view app_vue3 as demo.")

    def bootstrap(self):
        """Add Bootstrap Sass scafolding"""
        Bootstrap().install()
        self.info("Bootstrap scaffolding installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )

    def tailwind2(self):
        """Add Tailwind CSS 2.X."""
        Tailwind().install()
        self.info("Tailwind CSS 2 scaffolding installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
