class DefaultType:
    def __init__(self, value):
        self.value = value

    def __getattr__(self, attr):
        return self.value

    def __call__(self, *args, **kwargs):
        return self.value

    def __eq__(self, other):
        if self.value is None:
            return other is self.value
        else:
            return other == self.value


class Optional:
    """Optional helper class that allow evaluting an expression which can be undefined without
    raising an expression but returning a default value (None)."""

    def __init__(self, obj, default=None):
        self.obj = obj
        self.default = default

    def __getattr__(self, attr):
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return DefaultType(self.default)

    def __call__(self, *args, **kwargs):
        return DefaultType(self.default)

    def instance(self):
        return self.obj
