from threading import Thread, Event
from abc import ABC


class BaseRunner(ABC):
    def __init__(self, settings):
        self._thread = Thread(target=self._execute, args=())
        self._stop_event = Event()
        self.settings = settings

    def _execute(self):
        pass

    def start(self):
        self._thread.start()
