class CanBroadcast:
    def broadcast_on(self):
        return None

    def broadcast_with(self):
        return vars(self)

    def broadcast_as(self):
        return self.__class__.__name__
