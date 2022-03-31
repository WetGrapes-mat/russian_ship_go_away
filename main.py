import pygame
import os
import time
import random
import json

import button

pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Load images
RED_SPACE_SHIP_S = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP_S = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP_S = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
BLUE_SPACE_SHIP_M = pygame.image.load(os.path.join("assets", "pixel_ship_blue_middle.png"))
BLUE_SPACE_SHIP_L = pygame.image.load(os.path.join("assets", "pixel_ship_blue_big.png"))
RED_SPACE_SHIP_L = pygame.image.load(os.path.join("assets", "pixel_ship_red_big.png"))
GREEN_SPACE_SHIP_L = pygame.image.load(os.path.join("assets", "pixel_ship_green_big.png"))
BIG_SHIP_S = pygame.image.load(os.path.join("assets", "pixel_boss_ship_small.png"))
BIG_SHIP_M = pygame.image.load(os.path.join("assets", "pixel_boss_ship_middle.png"))
BIG_SHIP_L = pygame.image.load(os.path.join("assets", "pixel_boss_ship_big.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

images_dict = {"RED_SPACE_SHIP_S": RED_SPACE_SHIP_S,
               "GREEN_SPACE_SHIP_S": GREEN_SPACE_SHIP_S,
               "BLUE_SPACE_SHIP_S": BLUE_SPACE_SHIP_S,
               "RED_SPACE_SHIP_L": RED_SPACE_SHIP_L,
               "GREEN_SPACE_SHIP_L": GREEN_SPACE_SHIP_L,
               "BLUE_SPACE_SHIP_M": BLUE_SPACE_SHIP_M,
               "BLUE_SPACE_SHIP_L": BLUE_SPACE_SHIP_L,
               "BIG_SHIP_S": BIG_SHIP_S,
               "BIG_SHIP_M": BIG_SHIP_M,
               "BIG_SHIP_L": BIG_SHIP_L,
               "RED_LASER": RED_LASER,
               "BLUE_LASER": BLUE_LASER,
               "GREEN_LASER": GREEN_LASER
               }
# Boosters
HEART_BOOSTER = pygame.image.load(os.path.join("assets", "pixel_heart.png"))
LAZER_BOOSTER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_rocket.png")),
                                       (WIDTH * 0.05, HEIGHT * 0.05))
HEALTH_BOOSTER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_health.png")),
                                        (60, 40))
# About png
ABOUT_IMG = pygame.image.load(os.path.join("assets", "about.png")).convert_alpha()

# Buttons img-s
START_BUTTON_img = pygame.image.load(os.path.join("assets", "start_menu.png")).convert_alpha()
ABOUT_BUTTON_img = pygame.image.load(os.path.join("assets", "about_menu.png")).convert_alpha()
LEADERBOARD_BUTTON_img = pygame.image.load(os.path.join("assets", "leaderboard_menu.png")).convert_alpha()
MAIN_MENU_BUTTON_img = pygame.image.load(os.path.join("assets", "menu_button.png")).convert_alpha()

# create button instances
START_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT / 2 - 200, START_BUTTON_img, 1)
ABOUT_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT / 2 - 100, ABOUT_BUTTON_img, 1)
LEADERBOARD_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT / 2, LEADERBOARD_BUTTON_img, 1)
MAIN_MENU_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT / 2 - ABOUT_IMG.get_height() / 2 + ABOUT_IMG.get_height()
                                 + 10, MAIN_MENU_BUTTON_img, 1)

exploasion_list = []
e1 = pygame.mixer.Sound("sounds/E1.wav")
e1.set_volume(0.1)
exploasion_list.append(e1)
e2 = pygame.mixer.Sound("sounds/E2.wav")
e2.set_volume(0.1)
exploasion_list.append(e2)
e3 = pygame.mixer.Sound("sounds/E3.wav")
e3.set_volume(0.1)
exploasion_list.append(e3)
e4 = pygame.mixer.Sound("sounds/E4.wav")
e4.set_volume(0.1)
exploasion_list.append(e4)
e5 = pygame.mixer.Sound("sounds/E5.wav")
e5.set_volume(0.1)
exploasion_list.append(e5)
e6 = pygame.mixer.Sound("sounds/E7.wav")
e6.set_volume(0.1)
exploasion_list.append(e6)
e7 = pygame.mixer.Sound("sounds/E8.wav")
e7.set_volume(0.1)
laser_s = pygame.mixer.Sound("sounds/laser.wav")
laser_s.set_volume(0.1)
farm_s = pygame.mixer.Sound("sounds/farm.wav")
farm_s.set_volume(0.1)
appear_s = pygame.mixer.Sound("sounds/appear.wav")
appear_s.set_volume(0.1)

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            laser_s.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.got_shoot()
                        if obj.get_hp() == 0:
                            objs.remove(obj)
                            play_exploasion_sound()
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))


class Enemy(Ship):
    COLOR_MAP = {}

    def __init__(self, color, health=100):
        super().__init__(0, 0, health)
        self.load_config()
        self.color = color
        self.lazer_vel = 5
        self.ship_img, self.laser_img, self.hp, self.CD, self.chance, self.velocity = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.set_starting_position(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))

    def load_config(self):
        with open('config_list.json', 'r', encoding="utf-8") as file_config:
            config_list = json.load(file_config)
            for k, v in config_list["config"].items():
                self.COLOR_MAP[k] = (
                    images_dict[v["ship_img"]],
                    images_dict[v["laser_img"]],
                    v["hp"],
                    v["CD"],
                    v["chance"],
                    v["velocity"]
                )

    def move(self):
        self.y += self.velocity

    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.lazer_vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.CD:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def set_starting_position(self, x, y):
        self.y = y
        self.x = x

    def got_shoot(self):
        self.hp -= 1

    def get_hp(self):
        return self.hp


class Boss(Enemy):
    BOSS_MAP = {
        "boss_s": 2,
        "boss_m": 4,
        "boss_l": 6
    }
    first_line = 200
    counter = -200

    def __init__(self, color):
        super().__init__(color)
        self.lazer_vel = 8
        self.ship_img, self.laser_img, self.hp, self.CD, self.chance, self.velocity = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.bullets = self.BOSS_MAP[color]
        self.set_starting_position(WIDTH / 2 - self.ship_img.get_width() / 2, -200)

    def move(self):
        if self.y < HEIGHT / 2 - self.ship_img.get_height() / 2:
            self.y += self.velocity * 2
        else:
            if self.first_line > 0:
                self.x -= self.velocity
                self.first_line -= 1
            else:
                if self.counter < 200:
                    self.x += self.velocity
                    self.counter += 1
                elif self.counter < 600:
                    self.x -= self.velocity
                    self.counter += 1
                    if self.counter == 600:
                        self.counter = -200

    def shoot(self):
        if self.cool_down_counter == 0:
            if self.bullets == 2:
                laser_1 = Laser(self.x + 10, self.y + 90, self.laser_img)
                laser_2 = Laser(self.x + 90, self.y + 90, self.laser_img)
                self.lasers.append(laser_1)
                self.lasers.append(laser_2)
            if self.bullets == 4:
                laser_1 = Laser(self.x + 10, self.y + 90, self.laser_img)
                laser_2 = Laser(self.x + 90, self.y + 90, self.laser_img)
                laser_3 = Laser(self.x, self.y + 70, self.laser_img)
                laser_4 = Laser(self.x + 100, self.y + 70, self.laser_img)
                self.lasers.append(laser_1)
                self.lasers.append(laser_2)
                self.lasers.append(laser_3)
                self.lasers.append(laser_4)
            if self.bullets == 6:
                laser_1 = Laser(self.x + 10, self.y + 90, self.laser_img)
                laser_2 = Laser(self.x + 90, self.y + 90, self.laser_img)
                laser_3 = Laser(self.x, self.y + 70, self.laser_img)
                laser_4 = Laser(self.x + 100, self.y + 70, self.laser_img)
                laser_5 = Laser(self.x - 20, self.y + 60, GREEN_LASER)
                laser_6 = Laser(self.x + 120, self.y + 60, GREEN_LASER)
                self.lasers.append(laser_1)
                self.lasers.append(laser_2)
                self.lasers.append(laser_3)
                self.lasers.append(laser_4)
                self.lasers.append(laser_5)
                self.lasers.append(laser_6)
            self.cool_down_counter = 1


def play_exploasion_sound():
    a = random.randrange(0, 6)
    exploasion_list[a].play()


class Booster:
    COLOR_MAP = {
        "hp": HEALTH_BOOSTER,
        "lz": LAZER_BOOSTER,
        "lv": HEART_BOOSTER
    }

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.last_life = 240
        self.booster_img = self.COLOR_MAP[type]
        self.type = type
        self.mask = pygame.mask.from_surface(self.booster_img)
        appear_s.play()

    def draw(self, window):
        window.blit(self.booster_img, (self.x, self.y))

    def get_width(self):
        return self.booster_img.get_width()

    def get_height(self):
        return self.booster_img.get_height()


class Game:
    ENEMY_MAP = {}

    def __init__(self):
        self.load_wave()
        self.FPS = 60
        self.boss_colider = 0
        self.level = 0
        self.lives = 5
        self.CURR_ENEMIES = []
        self.CURR_BOOSTERS = []
        self.booster_effect = 0
        self.player_vel = 5
        self.lazer_vel = 5

    def load_wave(self):
        with open('wave_list.json', 'r', encoding="utf-8") as file_config:
            wave_list = json.load(file_config)
            for k, v in wave_list["wave"].items():
                temp_wave = []
                for name, many in v.items():
                    for i in range(int(many)):
                        temp_wave.append(Enemy(name))
                self.ENEMY_MAP[int(k)] = temp_wave

    def Loop_actions(self, player):
        self.Level_check()
        self.Random_booster()
        self.Enemy_behavior(player)
        self.Boosters_behavior(player)

    def Draw_objects(self, window):
        for enemy in self.CURR_ENEMIES:
            enemy.draw(window)
        for booster in self.CURR_BOOSTERS:
            booster.draw(WIN)

    def Level_check(self):
        if len(self.CURR_ENEMIES) == 0:
            self.level += 1
            if self.level < 19:
                self.CURR_ENEMIES = self.ENEMY_MAP[self.level]
            else:
                self.CURR_ENEMIES = self.ENEMY_MAP[18]
                for i in range(self.level - 18 + 1):
                    self.CURR_ENEMIES.append(Enemy("red_s"))
                    self.CURR_ENEMIES.append(Enemy("blue_s"))
                    self.CURR_ENEMIES.append(Enemy("green_s"))
                    self.CURR_ENEMIES.append(Enemy("blue_m"))
                    self.CURR_ENEMIES.append(Enemy("red_b"))
                    self.CURR_ENEMIES.append(Enemy("blue_b"))
                    self.CURR_ENEMIES.append(Enemy("green_b"))
            if self.level % 5 != 0:
                for enemy in self.CURR_ENEMIES:
                    enemy.set_starting_position(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))

    def Random_booster(self):
        if random.randrange(0, 6 * 60) == 1:
            booster = Booster(random.randrange(50, WIDTH - 100), random.randrange(100, HEIGHT - 100),
                              random.choice(["hp", "lz", "lv"]))
            self.CURR_BOOSTERS.append(booster)

    def Enemy_behavior(self, player):
        for enemy in self.CURR_ENEMIES[:]:
            enemy.move()
            enemy.move_lasers(player)

            if random.randrange(0, enemy.chance * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                if (enemy.color != "boss_s") and (enemy.color != "boss_m") and (enemy.color != "boss_l"):
                    player.health -= 10
                    self.CURR_ENEMIES.remove(enemy)
                    play_exploasion_sound()
                else:
                    if self.boss_colider == 0:
                        player.health -= 10
                        self.boss_colider = 120
            elif enemy.y + enemy.get_height() > HEIGHT:
                self.lives -= 1
                self.CURR_ENEMIES.remove(enemy)

    def Boosters_behavior(self, player):
        for booster in self.CURR_BOOSTERS:
            if collide(booster, player):
                if booster.type == "hp":
                    player.health = 100
                elif booster.type == "lz":
                    player.COOLDOWN = player.COOLDOWN / 2
                    self.booster_effect = 500
                elif booster.type == "lv":
                    self.lives += 1
                self.CURR_BOOSTERS.remove(booster)
                farm_s.play()

            booster.last_life -= 1

            if booster.last_life <= 0:
                self.CURR_BOOSTERS.remove(booster)

        if self.booster_effect > 0:
            self.booster_effect -= 1
        else:
            player.COOLDOWN = 30

        if self.boss_colider > 0:
            self.boss_colider -= 1


def main():
    game = Game()
    run = True
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    pygame.mixer.music.load("sounds/main.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    player = Player(WIDTH / 2, HEIGHT / 2)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {game.lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {game.level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        game.Draw_objects(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(game.FPS)
        redraw_window()

        if game.lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > game.FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - game.player_vel > 0:  # left
            player.x -= game.player_vel
        if keys[pygame.K_d] and player.x + game.player_vel + player.get_width() < WIDTH:  # right
            player.x += game.player_vel
        if keys[pygame.K_w] and player.y - game.player_vel > 0:  # up
            player.y -= game.player_vel
        if keys[pygame.K_s] and player.y + game.player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += game.player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        game.Loop_actions(player)

        player.move_lasers(-game.lazer_vel, game.CURR_ENEMIES)


def starting_titles():
    title_title_font = pygame.font.Font('fonts/Starjedi.ttf', 70)
    title_main_font = pygame.font.SysFont("arial", 50)

    pygame.mixer.music.load("sounds/beginning.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    title_text = title_title_font.render("Star Wars", 1, (255, 232, 31))
    main_text1 = title_main_font.render("Группа 021704 успешно закончила", 1, (255, 232, 31))
    main_text2 = title_main_font.render("бой за первый курс.", 1, (255, 232, 31))
    main_text3 = title_main_font.render("Но перед смелыми повстанцами", 1, (255, 232, 31))
    main_text4 = title_main_font.render("встала новая угроза: ", 1, (255, 232, 31))
    main_text5 = title_main_font.render("кафедра ИИТ. В первом ", 1, (255, 232, 31))
    main_text6 = title_main_font.render("тяжелом и продолжительном ", 1, (255, 232, 31))
    main_text7 = title_main_font.render("бою они потеряли несколько ", 1, (255, 232, 31))
    main_text8 = title_main_font.render("сильных бойцов. Позже", 1, (255, 232, 31))
    main_text9 = title_main_font.render("они были окружены войсками ", 1, (255, 232, 31))
    main_text10 = title_main_font.render("деканата и лишились еще ", 1, (255, 232, 31))
    main_text11 = title_main_font.render("половины союзников. Во второй битве ", 1, (255, 232, 31))
    main_text12 = title_main_font.render("нашим героям предстоит ", 1, (255, 232, 31))
    main_text13 = title_main_font.render("стокнуться с еще большей", 1, (255, 232, 31))
    main_text14 = title_main_font.render("силой империи ИИТ.", 1, (255, 232, 31))
    main_text15 = title_main_font.render("Сможет ли принцесcа Ксю", 1, (255, 232, 31))
    main_text16 = title_main_font.render("с её немногочисленным войском", 1, (255, 232, 31))
    main_text17 = title_main_font.render("пройти и это испытание?", 1, (255, 232, 31))

    WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 1000))
    WIN.blit(main_text1, (WIDTH / 2 - main_text1.get_width() / 2, 1000 + title_text.get_height() + 20))
    WIN.blit(main_text2, (WIDTH / 2 - main_text2.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 1))
    WIN.blit(main_text3, (WIDTH / 2 - main_text3.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 2))
    WIN.blit(main_text4, (WIDTH / 2 - main_text4.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 3))
    WIN.blit(main_text5, (WIDTH / 2 - main_text5.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 4))
    WIN.blit(main_text6, (WIDTH / 2 - main_text6.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 5))
    WIN.blit(main_text7, (WIDTH / 2 - main_text7.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 6))
    WIN.blit(main_text8, (WIDTH / 2 - main_text8.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 7))
    WIN.blit(main_text9, (WIDTH / 2 - main_text9.get_width() / 2, 1000 + title_text.get_height() + 20
                          + main_text1.get_height() * 8))
    WIN.blit(main_text10, (WIDTH / 2 - main_text10.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 9))
    WIN.blit(main_text11, (WIDTH / 2 - main_text11.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 10))
    WIN.blit(main_text12, (WIDTH / 2 - main_text12.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 11))
    WIN.blit(main_text13, (WIDTH / 2 - main_text13.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 12))
    WIN.blit(main_text14, (WIDTH / 2 - main_text14.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 13))
    WIN.blit(main_text15, (WIDTH / 2 - main_text15.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 14))
    WIN.blit(main_text16, (WIDTH / 2 - main_text16.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 15))
    WIN.blit(main_text17, (WIDTH / 2 - main_text17.get_width() / 2, 1000 + title_text.get_height() + 20
                           + main_text1.get_height() * 16))

    for i in range(1200):
        WIN.blit(BG, (0, 0))
        WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 1000 - 2 * i))
        WIN.blit(main_text1, (WIDTH / 2 - main_text1.get_width() / 2, 1000 + title_text.get_height() + 20 - 2 * i))
        WIN.blit(main_text2, (WIDTH / 2 - main_text2.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 1 - 2 * i))
        WIN.blit(main_text3, (WIDTH / 2 - main_text3.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 2 - 2 * i))
        WIN.blit(main_text4, (WIDTH / 2 - main_text4.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 3 - 2 * i))
        WIN.blit(main_text5, (WIDTH / 2 - main_text5.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 4 - 2 * i))
        WIN.blit(main_text6, (WIDTH / 2 - main_text6.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 5 - 2 * i))
        WIN.blit(main_text7, (WIDTH / 2 - main_text7.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 6 - 2 * i))
        WIN.blit(main_text8, (WIDTH / 2 - main_text8.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 7 - 2 * i))
        WIN.blit(main_text9, (WIDTH / 2 - main_text9.get_width() / 2, 1000 + title_text.get_height() + 20
                              + main_text1.get_height() * 8 - 2 * i))
        WIN.blit(main_text10, (WIDTH / 2 - main_text10.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 9 - 2 * i))
        WIN.blit(main_text11, (WIDTH / 2 - main_text11.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 10 - 2 * i))
        WIN.blit(main_text12, (WIDTH / 2 - main_text12.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 11 - 2 * i))
        WIN.blit(main_text13, (WIDTH / 2 - main_text13.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 12 - 2 * i))
        WIN.blit(main_text14, (WIDTH / 2 - main_text14.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 13 - 2 * i))
        WIN.blit(main_text15, (WIDTH / 2 - main_text15.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 14 - 2 * i))
        WIN.blit(main_text16, (WIDTH / 2 - main_text16.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 15 - 2 * i))
        WIN.blit(main_text17, (WIDTH / 2 - main_text17.get_width() / 2, 1000 + title_text.get_height() + 20
                               + main_text1.get_height() * 16 - 2 * i))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def about_page():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        WIN.blit(ABOUT_IMG, (WIDTH/2 - ABOUT_IMG.get_width() / 2, HEIGHT / 2 - ABOUT_IMG.get_height() / 2))

        if MAIN_MENU_BUTTON.draw(WIN):
            run = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        if START_BUTTON.draw(WIN):
            starting_titles()
            main()
        if ABOUT_BUTTON.draw(WIN):
            about_page()
        if LEADERBOARD_BUTTON.draw(WIN):
            pass
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #if event.type == pygame.MOUSEBUTTONDOWN:
            #    # starting_titles()
            #    main()
    pygame.quit()


main_menu()
