from abc import ABC, abstractmethod


class Direction:
    pass

class Up(Direction):
    pass

class Down(Direction):
    pass

class Left(Direction):
    pass

class Right(Direction):
    pass

class Event:
    def __init__(self, direction: Direction) -> None:
        self.direction = direction

class KeyboardEvent(Event):
    def __init__(self, direction: Direction) -> None:
        super().__init__(direction)

class VoiceEvent(Event):
    def __init__(self, direction: Direction) -> None:
        super().__init__(direction)

class EventFactory(ABC):
    @abstractmethod
    def new_voice_event(direction):
        return VoiceEvent(direction)

    @abstractmethod
    def new_keyboard_event(direction):
        return KeyboardEvent(direction)
