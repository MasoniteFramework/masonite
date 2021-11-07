class TestResponseCapsule:
    def __init__(self, base_test_response_class):
        self.base_test_response_class = base_test_response_class
        self.test_responses_classes = []

    def add(self, *classes):
        self.test_responses_classes.extend(classes)
        return self

    def build(self, *args):
        """Apply other test response class as mixins to base test response class."""
        obj = self.base_test_response_class(*args)
        for cls in self.test_responses_classes:
            base_cls = obj.__class__
            base_cls_name = obj.__class__.__name__
            obj.__class__ = type(base_cls_name, (base_cls, cls), {})
        return obj
