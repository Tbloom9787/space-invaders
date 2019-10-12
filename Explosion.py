from Settings import Settings


class Explosion:
    def __init__(self, sprite_sheet, screen, index_1=0, index_2=0, index_3=0, index_4=0):
        self.rect = None
        self.screen = screen
        self.fps = Settings.fps

        self.explosion_done = False
        self.sprite_sheet = sprite_sheet
        self.explosion_index = [index_1, index_2, index_3, index_4]
        self.explosion_start_index = 0
        self.frame_count = len(self.explosion_index)
        self.frame_counter = 0

        self.ship_exp_index = 0
        self.ship_exp_index_end = 8

    def draw_explosion(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect,
                         self.sprite_sheet.cell_list[self.explosion_index[self.explosion_start_index]])

        if self.explosion_start_index == 3:
            self.explosion_done = True
        else:
            self.explosion_start_index += 1

    def draw_ship_explosion(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect,
                         self.sprite_sheet.cell_list[self.ship_exp_index])
        self.ship_exp_index += 1

        if self.ship_exp_index >= 8:
            self.explosion_done = True
