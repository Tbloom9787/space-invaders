import pygame


class HighScores:
    def __init__(self):
        self.score_list = []

    def update_scores(self):
        self.score_list.clear()

        with open(r"Scores/High_Scores.txt", "r+") as f:
            data = f.readlines()
            for line in data:
                self.score_list.append(int(line.strip("\n")))

        self.score_list.sort(reverse = True)

    def add_score(self, score):
        with open("Scores/High_Scores.txt", "a") as myFile:
            myFile.write("\n" + score)
            myFile.close()


class Text:
    def __init__(self, screen, text, font_color, background_color,
                 rect_position_x, rect_position_y, font_size):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.font_color = font_color
        self.background_color = background_color
        self.font = pygame.font.SysFont(None, font_size)
        self.text = self.font.render(text, True, font_color, background_color)
        self.textrect = self.text.get_rect()
        self.textrect.x = rect_position_x
        self.textrect.y = rect_position_y

    def display_text(self):
        self.screen.blit(self.text, self.textrect)

    def change_text(self, text):
        self.text = self.font.render(text, True, self.font_color, self.background_color)


class HighScores_Display:
    def __init__(self, screen):
        self.screen = screen
        self.screen_area = screen.get_rect()
        self.high_scores = HighScores()
        self.scores_title = Text(screen, "HIGH SCORES", (0, 255, 0), (0, 0, 0),
                                    self.screen_area.w, self.screen_area.h, 100)
        self.set_text_position_menu(self.scores_title, 4, 6, 100)
        self.backspace_text = Text(screen, "Press Backspace To Return", (0, 255, 0), (0, 0, 0),
                                   self.screen_area.w, self.screen_area.h, 30)
        self.set_text_position_menu(self.backspace_text, 4, 6, 200, 80)
        self.scores_txt = []
        self.y = 250

        self.position_scores()

    def position_scores(self):

        self.y = 250

        self.scores_txt.clear()
        self.high_scores.score_list.clear()
        self.high_scores.update_scores()

        for line in self.high_scores.score_list:
            self.scores_txt.append(Text(self.screen, str(line), (255, 255, 255), (0, 0, 0),
                                        self.screen_area.w, self.y, 48))
            self.y += 50
        for line in self.scores_txt:
            self.set_text_position_menu(line, 2, 1, -100, 0)

    def set_text_position_menu(self, text, x_div, y_div, x_offset = 0, y_offset = 0):
        text.textrect.x = (text.textrect.x / x_div) + x_offset
        text.textrect.y = (text.textrect.y / y_div) + y_offset

    def draw_high_scores(self):
        self.scores_title.display_text()
        self.backspace_text.display_text()

        for line in self.scores_txt:
            line.display_text()

        pygame.display.update()
