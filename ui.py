import event_factory as events
import pygame
import threading
import time


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
        threading.Thread(target=self.get_events).start()

    def get_events(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print("Key A has been pressed")

                    if event.key == pygame.K_UP:
                        events.EventFactory.new_keyboard_event(events.Up()) 
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        print("Key A has been released")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # 1 == left button
                        print(f"left-click at {event.pos}")

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
