from .WebGuard import WebGuard
from ...helpers import config
from ...app import App

class Guard:

    guards = {}

    def __init__(self, app: App):
        self.app = app

    def register(self, key, cls):
        self.guards.update({key: cls})

    def make(self, key):
        if key in self.guards:
            self._guard = self.app.resolve(self.guards[key])
            return self._guard

    def set(self, key):
        return self.make(key)

    def get(self):
        return self._guard

    def driver(self, key):
        return self._guard.make(key)

    def register_guard(self, guard, cls):
        self.guards.update({guard: cls})

    def login(self, *args, **kwargs):
        return self._guard.login(*args, **kwargs)
    
    def user(self, *args, **kwargs):
        return self._guard.user(*args, **kwargs)
    
    def register(self, *args, **kwargs):
        return self._guard.register(*args, **kwargs)
    
    def __getattr__(self, key, *args, **kwargs):
        return getattr(self._guard, key)
