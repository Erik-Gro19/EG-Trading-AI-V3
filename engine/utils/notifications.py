# engine/utils/notifications.py

from collections import deque

class NotificationBus:
    def __init__(self, maxlen=100):
        self.events = deque(maxlen=maxlen)
        self.subscribers = []

    def notify(self, message, level="info"):
        """
        level: info, warning, error, success
        """
        self.events.appendleft((level, message))
        for cb in self.subscribers:
            cb(level, message)

    def get_events(self):
        return list(self.events)

    def subscribe(self, callback):
        self.subscribers.append(callback)
