import sys
import random
import pygame
from time import sleep

from Bullet import Bullet
from Alien import Alien
from Explosion import Explosion
from Mothership import MotherShip
from Sounds import Sounds
from Bunker import Bunker

sounds_music_start = Sounds("Sounds/spaceinvaders.wav")
sounds_explosion = Sounds("Sounds/explosion.wav")
sounds_music_mid = Sounds("Sounds/laserattack_music_mid.wav")
sounds_music_end = Sounds("Sounds/laserattack_music_end.mp3")
sounds_shot = Sounds("Sounds/shoot.wav")


def check_keydown_events(event, ai_settings, screen, ship, bullets, sprite_sheet, stats, sb, play_button,
                         aliens, mouse_x, mouse_y, bunkers):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, sprite_sheet)
        # Here
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RETURN:
        check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,
                          sprite_sheet, bunkers)
        stats.game_active = True
        stats.menu_active = False
        stats.high_score_active = False
        sounds_music_start.play_music()
    elif event.key == pygame.K_h:
        stats.game_active = False
        stats.menu_active = False
        stats.high_score_active = True
    elif event.key == pygame.K_BACKSPACE:
        stats.game_active = False
        stats.menu_active = True
        stats.high_score_active = False


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, sprite_sheet, bunkers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            mouse_x = 0
            mouse_y = 0
            check_keydown_events(event, ai_settings, screen, ship, bullets, sprite_sheet, stats, sb, play_button,
                                 aliens, mouse_x, mouse_y, bunkers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            sounds_music_start.play_music()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y, sprite_sheet, bunkers)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y, sprite_sheet, bunkers):
    if not stats.game_active:
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens, sprite_sheet)
        ship.center_ship()

        create_bunker_row(ai_settings, screen, ship, aliens, bunkers)

        ai_settings.first_switch = False
        ai_settings.second_switch = False


def fire_bullet(ai_settings, screen, ship, bullets, sprite_sheet):
    if len(bullets) < ai_settings.bullets_allowed:
        sounds_shot.play_sound()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def alien_shoot(ai_settings, screen, alien, sprite_sheet, alien_bullets, stats):
    shoot_rand = random.randint(1, ai_settings.alien_shoot_rng - ai_settings.alien_subtract_rng * stats.level)

    if shoot_rand <= 1:
        new_bullet = Bullet(ai_settings, screen, alien)
        alien_bullets.add(new_bullet)


def alien_bullet_update(alien_bullets, ai_settings, ship, explosions, sprite_sheet, screen, stats, sb,
                        ship_explosions_sheet, ship_explosions):
    for bullet in alien_bullets.copy():
        bullet.y += bullet.speed_factor
        bullet.rect.y = bullet.y
        bullet.draw_bullet()

        if bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(bullet)
        elif bullet.rect.y >= ship.rect.y and ship.rect.right >= bullet.rect.x >= ship.rect.left:
            alien_bullets.remove(bullet)
            new_explosion = Explosion(ship_explosions_sheet, screen)
            new_explosion.rect = pygame.Rect(ship.rect)
            new_explosion.rect.centerx = ship.rect.centerx
            ship_explosions.append(new_explosion)
            ship.ship_destroyed = True
            stats.ships_left -= 1
            sb.prep_ships()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, explosions, sprite_sheet, alien_bullets, main_menu, mother_ship, high_score_screen,
                  bunkers,
                  explosion, mother_ships, high_scores_screen, ship_explosions_sheet, ship_explosions):
    if stats.ships_left < 0:
        high_score_screen.high_scores.add_score(str(stats.score))
        high_scores_screen.position_scores()
        stats.menu_active = False
        stats.game_active = False
        stats.high_score_active = True

    check_bunker_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets,
                                   explosion, sprite_sheet, mother_ships, bunkers, alien_bullets)
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    for alien in aliens.sprites():
        alien.blit_me()
        alien_shoot(ai_settings, screen, alien, sprite_sheet, alien_bullets, stats)

    alien_bullet_update(alien_bullets, ai_settings, ship, explosions, sprite_sheet, screen, stats, sb,
                        ship_explosions_sheet, ship_explosions)

    for special in mother_ship:
        special.movement()
        special.blit_me()
        if special.rect.x > ai_settings.screen_width:
            mother_ship.remove(special)

    for bunker in bunkers.sprites():
        bunker.display_bunker()

    for exp in explosions:
        sounds_explosion.play_sound()
        exp.draw_explosion()
        if exp.explosion_done:
            explosions.remove(exp)

    for exp in ship_explosions:
        sounds_explosion.play_sound()
        exp.draw_ship_explosion()
        if exp.explosion_done:
            ship_explosions.remove(exp)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

    if len(aliens) < 30 and not ai_settings.first_switch:
        sounds_music_start.stop_music()
        sounds_music_mid.play_music()
        ai_settings.first_switch = True

    if len(aliens) < 15 and not ai_settings.second_switch:
        sounds_music_mid.stop_music()
        sounds_music_end.play_music()
        ai_settings.second_switch = True


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosion, sprite_sheet,
                   mother_ships, bunkers, alien_bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, explosion, sprite_sheet, mother_ships, bunkers)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bunker_bullet_collisions(ai_settings, screen, stats, sb, ship,
                                   aliens, bullets, explosions, sprite_sheet, mother_ships, bunkers, alien_bullets):
    collisions = pygame.sprite.groupcollide(bunkers, bullets, False, True)
    for hit in collisions:
        hit.bunker_damage()
        if hit.index >= hit.index_max:
            new_explosion = Explosion(sprite_sheet, screen, 3, 4, 6, 7)
            new_explosion.rect = pygame.Rect(hit.rect)
            new_explosion.rect.centerx = hit.rect.centerx
            explosions.append(new_explosion)
            bunkers.remove(hit)

    collisions = pygame.sprite.groupcollide(bunkers, alien_bullets, False, True)
    for hit in collisions:
        hit.bunker_damage()
        if hit.index >= hit.index_max:
            new_explosion = Explosion(sprite_sheet, screen, 3, 4, 6, 7)
            new_explosion.rect = pygame.Rect(hit.rect)
            new_explosion.rect.centerx = hit.rect.centerx
            explosions.append(new_explosion)
            bunkers.remove(hit)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, explosions, sprite_sheet, mother_ships, bunkers):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    for hit in collisions:
        new_explosion = Explosion(sprite_sheet, screen, 15, 16, 18, 19)
        new_explosion.rect = pygame.Rect(hit.rect)
        new_explosion.rect.centerx = hit.rect.centerx
        explosions.append(new_explosion)
        stats.score += hit.points

    if collisions:
        for aliens in collisions.values():
            sb.prep_score()
        check_high_score(stats, sb)

    collisions_special = pygame.sprite.groupcollide(mother_ships, bullets, True, True)
    for hit in collisions_special:
        new_explosion = Explosion(sprite_sheet, screen, 9, 10, 12, 13)
        new_explosion.rect = pygame.Rect(hit.rect)
        new_explosion.rect.centerx = hit.rect.centerx
        explosions.append(new_explosion)

    if collisions_special:
        for aliens in collisions_special.values():
            stats.score += ai_settings.special_alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()

        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()
        ai_settings.first_switch = False
        ai_settings.second_switch = False
        sounds_music_start.play_music()

        create_fleet(ai_settings, screen, ship, aliens, sprite_sheet)
        create_bunker_row(ai_settings, screen, ship, aliens, bunkers)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sprite_sheet, high_scores_screen):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

    else:
        pygame.mouse.set_visible(True)

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens, sprite_sheet)
    ship.center_ship()
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets, sprite_sheet, high_scores_screen):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sprite_sheet, high_scores_screen)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, sprite_sheet, mother_ship,
                  high_scores_screen):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sprite_sheet, high_scores_screen)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, sprite_sheet, high_scores_screen)

    spawn_rng = random.randint(0, 20000)
    if spawn_rng <= ai_settings.mother_ship_spawn_rate:
        new_mother_ship = MotherShip(screen, sprite_sheet)
        mother_ship.add(new_mother_ship)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (4 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, sprite_sheet):
    alien = Alien(ai_settings, screen, sprite_sheet)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height * 4 + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, sprite_sheet):
    alien = Alien(ai_settings, screen, sprite_sheet)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number, sprite_sheet)


def create_bunker_row(ai_settings, screen, ship, aliens, bunkers):
    num_of_bunkers = 6
    bunk_spawn = ai_settings.screen_width / num_of_bunkers

    for bunk in range(num_of_bunkers):
        new_bunker = Bunker(screen)
        new_bunker.rect.y = ship.rect.y - ship.rect.w
        new_bunker.rect.x = bunk_spawn * bunk
        bunkers.add(new_bunker)