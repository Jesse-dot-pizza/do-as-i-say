import game_model
import ui
import event_factory as events


class Controller:
    def __init__(self) -> None:
        self.ui = ui.SimpleUI()
        self.game_model = game_model.GameModel()

    def game_loop(self):
        self.ui.show_prompts(self.game_model.sample_level.current_expected_pair)
        voice_response, hardware_response = self.wait_for_response()
        result = self.game_model.evaluate_responses(voice_response, hardware_response)
        self.ui.play_feedback(result)
        
    def wait_for_response(self):
        sample_response_pair =  (events.VoiceEvent(events.Down), events.KeyboardEvent(events.Up))
        #later this will be something else, obvs.
        return sample_response_pair


controller = Controller()
controller.game_loop()