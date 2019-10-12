import pygame
from pygame.sprite import Group

import Functionality as gf
from Settings import Settings
from Scoreboard import GameStats
from Scoreboard import Scoreboard
from Sprite import SpriteSheet
from Button import Button
from Ship import Ship
from Menu import Main_Menu
from HighScores import HighScores_Display


def run_game():
    # Initialize pygame and settings
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create clock for  the timer
    clock = pygame.time.Clock()

    # Initialize button
    play_button = Button(screen, "Play")

    # Load Sprite Sheet and game score settings
    sprite_sheet = SpriteSheet("images/SpriteSheet/Space_Invaders_SS.png", 7, 3)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats, sprite_sheet)
    bg_color = (0, 0, 0)

    # Create an instance of ship, aliens, and bullets
    ship = Ship(ai_settings, screen, sprite_sheet)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    explosions = []
    ship_explosions = []
    mother_ship = Group()
    bunkers = Group()

    # Display menu
    main_menu = Main_Menu(screen, sprite_sheet)
    high_scores_screen = HighScores_Display(screen)

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens, sprite_sheet)
    ship_explosions_sheet = SpriteSheet("images/SpriteSheet/Ship_Explosion_2.png", 6, 2)

    # While Loop - runs the game until user exits
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets, sprite_sheet, bunkers)

        if stats.game_active:
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                             bullets, play_button, explosions, sprite_sheet, alien_bullets, main_menu, mother_ship,
                             high_scores_screen, bunkers, explosions, mother_ship, high_scores_screen,
                             ship_explosions_sheet, ship_explosions)
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets, explosions, sprite_sheet, mother_ship, bunkers, alien_bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets, sprite_sheet, mother_ship, high_scores_screen)
        elif stats.menu_active:
            screen.fill(bg_color)
            main_menu.render_menu()
        elif stats.high_score_active:
            screen.fill(bg_color)
            high_scores_screen.draw_high_scores()

        clock.tick(Settings.fps)


if __name__ == '__main__':
    run_game()
