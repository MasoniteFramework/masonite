from abc import abstractmethod


class StaticallyCallable(type):
    def __getattr__(self, attribute, *args, **kwargs):
        from wsgi import container
        instance = container.make(self.__service__)
        return getattr(instance, attribute)


class Mockable():
    """A mixin to define a service as mockable, to be able to quickly test
    the service with its fakeable implementation.
        Service.fake()
        # tests...
        Service.restore()
    This can be done inside a unit tests or defined globally in setUp() / tearDown() methods
    of a test case.
    """

    __service__ = ""

    # def __getattr__(self, attribute, *args, **kwargs):
    #     from wsgi import container
    #     import pdb ; pdb.set_trace()
    #     instance = container.make(self.__service__)
    #     return getattr(instance, attribute)

    @abstractmethod
    def get_mock_class():
        raise NotImplementedError(
            "get_mock_class() method must be implemented for a mockable service."
        )

    @classmethod
    def fake(cls):
        from wsgi import container
        mock_instance = cls.get_mock_class()(container)
        container.bind(cls.__service__, mock_instance)
        return mock_instance

    @classmethod
    def restore(cls):
        from wsgi import container
        try:
            original_instance = cls(container)
        except TypeError:
            original_instance = cls()
        container.bind(cls.__service__, original_instance)
        return original_instance
