import event_factory as events

sample_level_data = [
    (events.Up, events.Down),
    (events.Down, events.Up),
    (events.Left, events.Right),
    (events.Right, events.Left)
]

class Level:
    def __init__(self, event_pairs: list, default_duration: float) -> None:
        self.event_pairs = event_pairs
        self.duration = default_duration



class GameModel:
    def __init__(self) -> None:
        self.current_level = Level(sample_level_data, 10)
        self.keystroke_data = None
        self.voice_data = None
        self.prompt_index = 0
        self.current_prompt = self.current_level.event_pairs[self.prompt_index]

    def evaluate_responses(self):
        




    