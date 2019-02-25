class NoneType:
    def __getattr__(self, attr):
        return None

    def __call__(self, *args, **kwargs):
        return None

    def __eq__(self, other):
        return other is None


class Optional:

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        # method = getattr(self.obj, attr)
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return NoneType()

    def __call__(self, *args, **kwargs):
        return NoneType()

    def instance(self):
        return self.obj
