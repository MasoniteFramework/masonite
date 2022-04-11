class DefaultType:
    def __init__(self, value, obj):
        self.value = value
        self.obj = obj

    def default(self):
        if callable(self.value):
            return self.value(self.obj)
        else:
            return self.value

    def __getattr__(self, attr):
        return self.default()

    def __call__(self, *args, **kwargs):
        return self.default()

    def __eq__(self, other):
        value = self.default()
        if value is None:
            return other is value
        else:
            return other == value


class Optional:
    """Optional helper class that allow evaluting an expression which can be undefined without
    raising an expression but returning a default value (None)."""

    def __init__(self, obj, default=None):
        self.obj = obj
        self.default = default

    def __getattr__(self, attr):
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return DefaultType(self.default, self.obj)()

    def __call__(self, *args, **kwargs):
        return DefaultType(self.default, self.obj)()

    def instance(self):
        return self.obj
