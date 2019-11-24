"""New Preset System Command."""
import os
import shutil

from cleo import Command
from ..commands.presets.React import React
from ..commands.presets.Vue import Vue
from ..commands.presets.Bootstrap import Bootstrap
from ..commands.presets.Remove import Remove

class PresetCommand(Command):
    """
    Swap the front-end scaffolding for the application

    preset
        {name : Name of the preset}
    """

    def handle(self):
        self.info('Scaffolding Application ...')
        preset_name = self.argument('name')
        if not preset_name in ['react', 'vue', 'remove', 'bootstrap']:
            raise ValueError('Invalid preset')
        return getattr(self, preset_name)()

    def remove(self):
        Remove().install()
        self.info('Frontend scaffolding removed successfully.')

    def react(self):
        React().install()
        self.info('React scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')

    def vue(self):
        Vue().install()
        self.info('Vue scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')

    def bootstrap(self):
        Bootstrap().install()
        self.info('Bootstrap scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')
