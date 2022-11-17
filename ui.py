import event_factory as events
import pygame
import threading
import time
import speech_recognition as sr
import pyaudio

window_dimensions = (500, 500)

class SimpleUI:
    def __init__(self) -> None:
        pygame.init()
        self.success_sound = pygame.mixer.Sound("sfx\clack.wav")
        self.fail_sound = pygame.mixer.Sound(r"sfx\boing.wav")


    def show_prompts(self, expected_values):
        print(expected_values)

    def play_feedback(self, event_result: bool):
        if event_result:
            self.success_sound.play()
        else:
            self.fail_sound.play()
        
class PygameWindow:
    def __init__(self) -> None:
        pygame.init()
        self.animation_in_progress = threading.RLock()
        self.seconds_between_frames = 0.2
        pygame.fastevent.init()
        threading.Thread(target=self.animate).start()

    def get_keyboard_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return events.EventFactory.new_keyboard_event(events.Up()) 
                if event.key == pygame.K_DOWN:
                    return events.EventFactory.new_keyboard_event(events.Down()) 
                if event.key == pygame.K_LEFT:
                    return events.EventFactory.new_keyboard_event(events.Left()) 
                if event.key == pygame.K_RIGHT:
                    return events.EventFactory.new_keyboard_event(events.Right())
                    print("Key A has been released")

    def animate(self):
        window = pygame.display.set_mode(window_dimensions)
        pygame.display.set_caption("Do as I say not as I do")
        running = True
        while running:
            starting_time = time.process_time()
            with self.animation_in_progress:
                window.fill((0,200,0))
   
                pygame.fastevent.pump()
                elapsed_time = time.process_time() - starting_time
                if elapsed_time < self.seconds_between_frames:
                    pygame.time.wait(round((self.seconds_between_frames - elapsed_time) * 1000))
                pygame.display.flip()

class SpeechRecognizer(sr.Recognizer):
    # note we going to have to not use the default google api key for production
    def __init__(self) -> None:
        super().__init__()
        self.mic = sr.Microphone()
        self.energy_threshold = 4000
        self.audio_data = None
    
    def listen_for_audio(self, seconds):
        with self.mic as source:
            audio_data = self.record(source, duration=seconds)
        self.audio_data = audio_data
        return audio_data

    def process_audio_data(self, audio_data: sr.AudioData):
        result = self.recognize_google(audio_data)
        return result

    def record_audio_to_wav(self):

        with self.mic as source:
            print("Say something!")
            audio = self.record(source, duration=10)

        # write audio to a WAV file
        with open("sfx\microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())


    def recognize_speech_from_mic(recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occured, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    def parse_response(self, response):
        words_detected = response["transcription"].split()
        if "up" in words_detected:
            return events.Up()
        elif "down" in words_detected:
            return events.Down()
        elif "left" in words_detected:
            return events.Left()
        elif "right" in words_detected:
            return events.Right()

pygame_window = PygameWindow()
speech_rec = SpeechRecognizer()



def get_responses():
    voice_response = speech_rec.listen_for_audio(10)
    speech_rec.process_audio_data(voice_response)

    return voice_response


result = get_responses()
print(result)