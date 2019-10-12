class Settings:
    fps = None

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        self.ship_limit = 3

        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 10

        self.fleet_drop_speed = 10
        self.alien_bullets_allowed = 1
        self.alien_shoot_rng = 500
        self.alien_subtract_rng = 200

        self.speedup_scale = .75
        self.score_scale = 1.5

        Settings.fps = 60
        self.mother_ship_spawn_rate = 5

        self.first_switch = False
        self.second_switch = False

        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.alien_points = 50
        self.special_alien_points = 1000

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
