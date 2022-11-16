from abc import ABC, abstractmethod
from collections import deque


class Event:
    pass

class Up(Event):
    pass

class Down(Event):
    pass

class Left(Event):
    pass

class Right(Event):
    pass

class EventFactory(ABC):
    @abstractmethod
    def new_voice_event(event: Event):
        event_queue.new_voice_event(event)

    @abstractmethod
    def new_keyboard_event(event: Event):
        event_queue.new_keyboard_event(event)


class EventQueue:
    def __init__(self) -> None:
        self.keyboard_events = deque()
        self.voice_events = deque()

    def new_keyboard_event(self, event: Event):
        self.keyboard_events.append(event)
    
    def new_voice_event(self, event: Event):
        self.voice_events.append(event)

event_queue = EventQueue()
