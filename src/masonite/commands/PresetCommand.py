"""New Preset System Command."""
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
        if preset_name not in ['react', 'vue', 'remove', 'bootstrap']:
            raise ValueError('Invalid preset')
        return getattr(self, preset_name)()

    def remove(self):
        """Removes frontend scaffolding"""
        Remove().install()
        self.info('Frontend scaffolding removed successfully.')

    def react(self):
        """Add React frontend while also removing Vue (if it was previously selected)"""
        React().install()
        self.info('React scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')

    def vue(self):
        """Add Vue frontend while also removing React (if it was previously selected)"""
        Vue().install()
        self.info('Vue scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')

    def bootstrap(self):
        """Add Bootstrap Sass scafolding"""
        Bootstrap().install()
        self.info('Bootstrap scaffolding installed successfully.')
        self.comment('Please run "npm install && npm run dev" to compile your fresh scaffolding.')
