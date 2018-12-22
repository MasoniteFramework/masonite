class Optional:

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        # method = getattr(self.obj, attr)
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return None
    
    def __call__(self, *args, **kwargs):
        return None

    def instance(self):
        return self.obj



class OptionalCall:

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        # method = getattr(self.obj, attr)
        if hasattr(self.obj, attr):
            return getattr(self.obj, attr)
        return self

    def __call__(self, *args, **kwargs):
        return None

    def instance(self):
        return self.obj
