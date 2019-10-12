import pygame


class Sounds:
    def __init__(self, sound_destination):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        self.sound_destination = sound_destination

    def play_music(self):
        pygame.mixer.music.load(self.sound_destination)
        pygame.mixer.music.play(-1)

    def play_sound(self):
        sound = pygame.mixer.Sound(self.sound_destination)
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()
