import event_factory as events
from pygame import mixer


class SimpleUI:
    def __init__(self) -> None:
        mixer.init()
        self.success_sound = mixer.Sound("sfx\clack.wav")
        self.fail_sound = mixer.Sound(r"sfx\boing.wav")

    def show_prompts(self, expected_values):
        print(expected_values)

    def play_feedback(self, event_result: bool):
        if event_result:
            self.success_sound.play()
        else:
            self.fail_sound.play()
        