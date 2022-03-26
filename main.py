import pygame
import os
import time
import random
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

# Boosters
HEART_BOOSTER = pygame.image.load(os.path.join("assets", "pixel_heart.png"))
LAZER_BOOSTER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_rocket.png")),
                                       (WIDTH * 0.05, HEIGHT * 0.05))
HEALTH_BOOSTER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_health.png")),
                                        (WIDTH * 0.05, HEIGHT * 0.05))

# Buttons img-s
START_BUTTON_img = pygame.image.load(os.path.join("assets", "start_menu.png")).convert_alpha()
ABOUT_BUTTON_img = pygame.image.load(os.path.join("assets", "about_menu.png")).convert_alpha()
LEADERBOARD_BUTTON_img = pygame.image.load(os.path.join("assets", "leaderboard_menu.png")).convert_alpha()
MAIN_MENU_BUTTON_img = pygame.image.load(os.path.join("assets", "start_menu.png")).convert_alpha()

# create button instances
START_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT/2 - 200, START_BUTTON_img, 1)
ABOUT_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT/2 - 100, ABOUT_BUTTON_img, 1)
LEADERBOARD_BUTTON = button.Button(WIDTH / 2 - 200 / 2, HEIGHT/2, LEADERBOARD_BUTTON_img, 1)
MAIN_MENU_BUTTON = button.Button(100, 200, MAIN_MENU_BUTTON_img, 1)

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
    COOLDOWN = 30

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

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

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

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
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
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP_S, RED_LASER),
        "green": (GREEN_SPACE_SHIP_S, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP_S, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def play_exploasion_sound():
    a = random.randrange(0, 6)
    exploasion_list[a].play()


class Booster:
    COLOR_MAP = {
        "hp": HEART_BOOSTER,
        "lz": LAZER_BOOSTER
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


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    boosters = []
    wave_length = 5
    enemy_vel = 1
    booster_effect = 0

    player_vel = 5
    laser_vel = 5

    pygame.mixer.music.load("sounds/main.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    player = Player(WIDTH/2, HEIGHT/2)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        for booster in boosters:
            booster.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        if random.randrange(0, 10 * 60) == 1:
            booster = Booster(random.randrange(50, WIDTH - 100), random.randrange(100, HEIGHT - 100),
                              random.choice(["hp", "lz"]))
            boosters.append(booster)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 5 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                play_exploasion_sound()
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        for booster in boosters:
            if collide(booster, player):
                if booster.type == "hp":
                    player.health = 100
                elif booster.type == "lz":
                    player.COOLDOWN = player.COOLDOWN/2
                    booster_effect = 300
                boosters.remove(booster)
                farm_s.play()

            booster.last_life -= 1

            if booster.last_life <= 0:
                boosters.remove(booster)

        if booster_effect > 0:
            booster_effect -= 1
        else:
            player.COOLDOWN = 30


        player.move_lasers(-laser_vel, enemies)


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


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        if START_BUTTON.draw(WIN):
            starting_titles()
            main()
        if ABOUT_BUTTON.draw(WIN):
            print('EXIT')
        if LEADERBOARD_BUTTON.draw(WIN):
            print('EXIT')
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                starting_titles()
                main()
    pygame.quit()


main_menu()
