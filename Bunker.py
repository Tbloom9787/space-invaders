import pygame
from Sprite import SpriteSheet
from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, screen):
        super(Bunker, self).__init__()
        self.bunker_animated = SpriteSheet("images/SpriteSheet/Bunker_Animated.png", 3, 3)
        self.index = 0
        self.index_max = 5
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 64, 64)

    def display_bunker(self):
        self.screen.blit(self.bunker_animated.sheet, self.rect,
                         self.bunker_animated.cell_list[self.index])

    def bunker_damage(self):
        if self.index < 5:
            self.index += 1
