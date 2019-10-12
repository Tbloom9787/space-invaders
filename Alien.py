import pygame
from pygame.sprite import Sprite
from Settings import Settings
import random


class Alien(Sprite):
    def __init__(self, ai_settings, screen, sprite_sheet):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.sprite_sheet = sprite_sheet

        self.image = pygame.image.load('Images/AlienInvader.bmp')
        self.rect = pygame.Rect(sprite_sheet.cell_list[0])

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.Ship_Sprite_Index = [5, 8, 11, 14, 17, 20]
        self.Explosion_Index = [16, 17, 19, 20]

        self.total_num_of_alien_Sprites = 3
        self.num_of_base_frames = len(self.Ship_Sprite_Index) / self.total_num_of_alien_Sprites
        self.frame_counter = 0
        self.frame_start = random.randint(0, 2) * 2

        if self.frame_start == 0:
            self.points = 10
        elif self.frame_start == 2:
            self.points = 20
        elif self.frame_start == 4:
            self.points = 30

        self.frame_counti = self.frame_start
        self.bullet_count_tracker = 0

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blit_me(self):
        self.frame_counter += 1

        if self.frame_counter % Settings.fps / 2 == 0:
            self.frame_counti += 1

            if self.frame_counti >= self.frame_start + 2:
                self.frame_counti = self.frame_start

        self.screen.blit(self.sprite_sheet.sheet, self.rect,
                         self.sprite_sheet.cell_list[self.Ship_Sprite_Index[self.frame_counti]])
