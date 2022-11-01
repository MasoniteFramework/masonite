import inspect
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ..foundation import Application


class Event:
    """Event manager class allowing to fire events, listen to events and register event
    listeners."""

    def __init__(self, application: "Application"):
        self.application = application
        self.events: dict = {}

    def get_events(self) -> dict:
        return self.events

    def listen(self, event: Any, listeners: "List[Any]|Any") -> "Event":
        """Listen to the given event with the given listener(s)."""
        if not isinstance(listeners, list):
            listeners = [listeners]

        if event in self.events:
            self.events[event] += listeners
        else:
            self.events.update({event: listeners})

        return self

    def fire(self, event: "str|Any", *args, **kwargs) -> List[Any]:
        """Fire the given event with payload if any."""
        if isinstance(event, str):
            collected_events = self.collect_events(event)
            for collected_event in collected_events:
                for listener in self.events.get(collected_event, []):
                    listener().handle(event, *args, **kwargs)
            return collected_events
        else:
            if inspect.isclass(event):
                lookup = event
                event = event()
            else:
                lookup = event.__class__
            for listener in self.events.get(lookup, []):
                listener().handle(event, *args, **kwargs)

            return [event]

    def collect_events(self, fired_event: str) -> List[Any]:
        """Collect all events listened to matching the searched event. Wildcards (*) can be used."""
        collected_events = []
        for stored_event in self.events.keys():

            if not isinstance(stored_event, str):
                continue

            if stored_event == fired_event:
                collected_events.append(fired_event)

            elif stored_event.endswith("*") and fired_event.startswith(
                stored_event.replace("*", "")
            ):
                collected_events.append(stored_event)

            elif stored_event.startswith("*") and fired_event.endswith(
                stored_event.replace("*", "")
            ):
                collected_events.append(stored_event)

            elif "*" in stored_event:
                starts, end = stored_event.split("*")
                if fired_event.startswith(starts) and fired_event.endswith(end):
                    collected_events.append(stored_event)

        return collected_events

    def subscribe(self, *listeners) -> None:
        """Subscribe a specific listener class to the events system."""
        for listener in listeners:
            listener.subscribe(self)
