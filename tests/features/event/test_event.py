import time

import pytest

from src.masonite.events import Event
from tests import TestCase


class UserAddedEvent(Event):
    def __init__(self):
        pass

    def handle(self):
        pass


class NewUserEvent(Event):
    def __init__(self):
        pass

    def handle(self):
        pass


class SendEmailListener:
    def handle(self, event):
        pass


class UpdateAdminListener:
    def handle(self, event, user):
        pass


class SendAlert:
    def handle(self, event):
        pass


class AdminNotificationListener:
    def handle(self):
        pass


class Subscriber:
    def handle(self, event):
        pass

    def subscribe(self, event):
        event.listen("masonite.event_handled", [self.__class__])


class TestEvent(TestCase):
    def setUp(self):
        super().setUp()
        self.event = self.application.make("event")
        self.event.listen(UserAddedEvent, [SendEmailListener])

    def test_events_registered(self):
        self.assertEqual(len(self.event.get_events().get(UserAddedEvent)), 2)
        self.event.listen(UserAddedEvent, [AdminNotificationListener])
        self.assertEqual(len(self.event.get_events().get(UserAddedEvent)), 3)

    def test_fire_event_class(self):
        self.event.fire(UserAddedEvent)

    def test_fire_event_string(self):
        self.event.listen("masonite.*.booted", [SendEmailListener])
        self.event.listen("masonite.commands", [SendEmailListener])
        self.event.listen("view.*", [SendEmailListener])
        self.event.listen("masonite.exception.*", [SendEmailListener])
        self.event.listen("user.added", [UpdateAdminListener])
        self.assertEqual(self.event.fire("masonite.commands"), ["masonite.commands"])
        self.assertEqual(self.event.fire("masonite.orm.booted"), ["masonite.*.booted"])
        self.assertEqual(self.event.fire("masonite.orm"), [])
        self.assertEqual(self.event.fire("masonite.command"), [])
        self.assertEqual(
            self.event.fire("masonite.exception.ZeroDivisionError"),
            ["masonite.exception.*"],
        )
        self.assertEqual(self.event.fire("view.rendered"), ["view.*"])
        self.assertEqual(self.event.fire("user.added", 1), ["user.added"])

    def test_fire_event_class(self):
        self.event.listen(NewUserEvent, [SendAlert])
        self.event.fire(NewUserEvent())

    def test_can_subscribe(self):
        self.event.subscribe(Subscriber())
        self.assertEqual(
            self.event.fire("masonite.event_handled"), ["masonite.event_handled"]
        )
