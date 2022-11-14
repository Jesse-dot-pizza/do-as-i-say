import event_factory as events

sample_level_data = [
    (events.VoiceEvent(events.Up), events.KeyboardEvent(events.Down)),
    (events.VoiceEvent(events.Down), events.KeyboardEvent(events.Up)),
    (events.VoiceEvent(events.Left), events.KeyboardEvent(events.Right)),
    (events.VoiceEvent(events.Right), events.KeyboardEvent(events.Left))
]

class Level:
    def __init__(self, event_pairs) -> None:
        self.expected_event_pairs = event_pairs
        self.current_pair_index = 0
        self.current_expected_pair = self.expected_event_pairs[self.current_pair_index]

    def select_next_pair(self):
        self.current_pair_index += 1
        self.current_expected_pair = self.expected_event_pairs[self.current_pair_index]


class GameModel:
    def __init__(self) -> None:
        self.sample_level = Level(sample_level_data)

    def evaluate_responses(self, voice_response, keyboard_response):
        if (voice_response, keyboard_response) is self.sample_level.current_expected_pair:
            return True

        else:
            return False


    