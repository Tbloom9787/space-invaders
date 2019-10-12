import pygame
from HighScores import Text
from Sprite import Sprite


class Main_Menu:
    def __init__(self, screen, sprite_sheet):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.sprite_sheet = sprite_sheet

        self.space_invaders_title = Text(screen, "SPACE INVADERS", (0, 255, 0), (0, 0, 0),
                                         self.screen_area.w, self.screen_area.h, 100)
        self.set_text_position_menu(self.space_invaders_title, 4, 6)

        self.press_enter_text = Text(screen, "Press Enter To Start Game", (0, 255, 0), (0, 0, 0),
                                     self.screen_area.w, self.screen_area.h, 30)
        self.set_text_position_menu(self.press_enter_text, 2, 4)

        self.press_highscores_text = Text(screen, "Press H To View High Scores", (0, 255, 0), (0, 0, 0),
                                          self.screen_area.w, self.screen_area.h, 30)
        self.set_text_position_menu(self.press_highscores_text, 2, 4, 0, 50)

        self.alien_points_1_text = Text(screen, "10 Points", (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.screen_area.h, 48)
        self.set_text_position_menu(self.alien_points_1_text, 2, 2, 0, -50)

        self.alien_points_2_text = Text(screen, "20 Points", (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.screen_area.h, 48)
        self.set_text_position_menu(self.alien_points_2_text, 2, 2)

        self.alien_points_3_text = Text(screen, "30 Points", (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.screen_area.h, 48)
        self.set_text_position_menu(self.alien_points_3_text, 2, 2, 0, 50)

        self.alien_points_4_text = Text(screen, "????????", (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.screen_area.h, 48)
        self.set_text_position_menu(self.alien_points_4_text, 2, 2, 0, 100)

        self.alien_1_sprite = Sprite(screen, sprite_sheet, 5,
                                     self.screen_area.w, self.screen_area.h)
        self.set_sprite_position_menu(self.alien_1_sprite, 2, 2, -100, -50)

        self.alien_2_sprite = Sprite(screen, sprite_sheet, 11,
                                     self.screen_area.w, self.screen_area.h)
        self.set_sprite_position_menu(self.alien_2_sprite, 2, 2, -100)

        self.alien_3_sprite = Sprite(screen, sprite_sheet, 17,
                                     self.screen_area.w, self.screen_area.h)
        self.set_sprite_position_menu(self.alien_3_sprite, 2, 2, -100, 50)

        self.alien_4_sprite = Sprite(screen, sprite_sheet, 0,
                                     self.screen_area.w, self.screen_area.h)
        self.set_sprite_position_menu(self.alien_4_sprite, 2, 2, -100, 100)

    def set_text_position_menu(self, text, x_div, y_div, x_offset=0, y_offset=0):
        text.textrect.x = (text.textrect.x / x_div) + x_offset
        text.textrect.y = (text.textrect.y / y_div) + y_offset

    def set_sprite_position_menu(self, sprite, x_div, y_div, x_offset=0, y_offset=0):
        sprite.rect_location.x = (sprite.rect_location.x / x_div) + x_offset
        sprite.rect_location.y = (sprite.rect_location.y / y_div) + y_offset

    def render_menu(self):
        self.space_invaders_title.display_text()
        self.press_enter_text.display_text()
        self.press_highscores_text.display_text()
        self.alien_points_1_text.display_text()
        self.alien_points_2_text.display_text()
        self.alien_points_3_text.display_text()
        self.alien_points_4_text.display_text()
        self.alien_1_sprite.blit_me()
        self.alien_2_sprite.blit_me()
        self.alien_3_sprite.blit_me()
        self.alien_4_sprite.blit_me()

        pygame.display.update()
