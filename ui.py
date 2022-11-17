import event_factory as events
import pygame
import threading
import time
import speech_recognition as sr
import pyaudio

window_dimensions = (500, 500)
     
class PygameWindow:
    def __init__(self) -> None:
        pygame.init()
        self.animation_in_progress = threading.RLock()
        self.seconds_between_frames = 0.2
        self.keyboard_commands = []
        pygame.fastevent.init()
        threading.Thread(target=self.animate).start()

    def get_keyboard_events(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyboard_commands.append(events.Up()) 
                if event.key == pygame.K_DOWN:
                    self.keyboard_commands.append(events.Down()) 
                if event.key == pygame.K_LEFT:
                    self.keyboard_commands.append(events.Left())
                if event.key == pygame.K_RIGHT:
                    self.keyboard_commands.append(events.Right())


    def listen_for_keystrokes(self, duration):
        self.keyboard_commands = []
        threading.Thread(target=self.get_keyboard_events).start()
        



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
    # TODO: we going to have to not use the default google api key for production
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
        words_detected = self.recognize_google(audio_data)
        result = self.create_events(words_detected)
        return result

    def create_events(self, words_detected: str):
        word_list = words_detected.split()
        output_commands = []
        for word in word_list:
            if word == "up":
                output_commands.append(events.Up())
            elif word == "down":
                output_commands.append(events.Down())
            elif word == "left":
                output_commands.append(events.Left())
            elif word == "right":
                output_commands.append(events.Right())
        return output_commands


pygame_window = PygameWindow()
speech_rec = SpeechRecognizer()



def get_responses():
    voice_response = speech_rec.listen_for_audio(10)
    speech_rec.process_audio_data(voice_response)

    return voice_response

