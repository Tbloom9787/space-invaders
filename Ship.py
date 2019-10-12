import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen, sprite_sheet):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = pygame.Rect(sprite_sheet.cell_list[0])
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

        self.sprite_sheet = sprite_sheet
        self.Ship_Sprite_Index = 1
        self.Explosion_Index = [4, 5, 7, 8]

        self.ship_destroyed = False

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        if not self.ship_destroyed:
            self.rect.centerx = self.center
        else:
            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom
            self.center = float(self.rect.centerx)
            self.ship_destroyed = False

    def blit_me(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect, self.sprite_sheet.cell_list[self.Ship_Sprite_Index])
