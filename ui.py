from pygame import mixer


class SimpleUI:
    def __init__(self) -> None:
        mixer.init()
        self.success_sound = mixer.Sound("sfx\clack.wav")
        self.fail_sound = mixer.Sound(r"sfx\boing.wav")

    