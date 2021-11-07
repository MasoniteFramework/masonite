class Facade(type):
    def __getattr__(self, attribute, *args, **kwargs):
        from wsgi import application

        return getattr(application.make(self.key), attribute)
