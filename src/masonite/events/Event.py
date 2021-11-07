""" Event Module """

import inspect


class Event:
    def __init__(self, application):
        """Event contructor
        Arguments:
            application - The Masonite application class
        """
        self.application = application
        self.events = {}

    def get_events(self):
        return self.events

    def listen(self, event, listeners):

        if not isinstance(listeners, list):
            listeners = [listeners]

        if event in self.events:
            self.events[event] += listeners
        else:
            self.events.update({event: listeners})

        return self

    def fire(self, event, *args, **kwargs):
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

    def collect_events(self, fired_event):
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

    def subscribe(self, *listeners):
        """Subscribe a specific listener object to the events system
        Raises:
            InvalidSubscriptionType -- raises when the subscribe attribute on the listener object is not a class.
        """
        for listener in listeners:
            listener.subscribe(self)
