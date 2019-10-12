import pygame


class Sprite:
    def __init__(self, screen, sprite_sheet, crop_index, rect_position_x, rect_position_y):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.crop_location = pygame.Rect(sprite_sheet.cell_list[crop_index])
        self.rect_location = pygame.Rect(0, 0, 32, 32)
        self.rect_location.x = rect_position_x
        self.rect_location.y = rect_position_y

    def blit_me(self):
        self.screen.blit(self.sprite_sheet.sheet, self.rect_location, self.crop_location)


class SpriteSheet:
    def __init__(self, filename, rows, cols):
        self.cols = cols
        self.rows = rows
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.total_cell_count = cols * rows
        self.rect = self.sheet.get_rect()
        self.cell_width = self.rect.width / cols
        self.cell_height = self.rect.height / rows
        self.cell_list = list([(index % cols * self.cell_width, int(index / cols) * self.cell_height,
                                self.cell_width, self.cell_height) for index in range(self.total_cell_count)])

    def sprite_sheet_log(self):
        for cells in self.cell_list:
            print(cells)
