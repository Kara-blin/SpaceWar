import pygame
import random

from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'soun')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceKiller")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 100))
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left+30, self.rect.centery)
                bullet2 = Bullet(self.rect.right-30, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -120 or self.rect.right > WIDTH + 120:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (25, 25 ))
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 10)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['bullet_upgrade', 'HP'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()
# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shootlaser.wav'))
shoot_sound.set_volume(0.3)
pow_sound = pygame.mixer.Sound(path.join(snd_dir, 'pick_up.wav'))
pow_sound.set_volume(0.3)
expl_sounds = []
for snd in ['boom.wav','boom1.wav','boom2.wav']:
    expl_sound = pygame.mixer.Sound(path.join(snd_dir, snd))
    expl_sound.set_volume(0.3)
    expl_sounds.append(expl_sound)


pygame.mixer.music.load(path.join(snd_dir, 'Megadrive_-_NARC_Hotline_Miami_2_Wrong_Number_OST_63637466.ogg'))
pygame.mixer.music.set_volume(0.4)
# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, 'Background1.png')).convert()
player_img = pygame.image.load(path.join(img_dir, "spaceship1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
powerup_images = {}
powerup_images['HP'] = pygame.image.load(path.join(img_dir, 'HP.png')).convert()
powerup_images['bullet_upgrade'] = pygame.image.load(path.join(img_dir, 'bullet_upgrade.png')).convert()
background_rect = background.get_rect()
meteor_images = []
meteor_list = ['asteroid1.png','asteroid1big.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(3):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (80, 80))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (72, 72))
    explosion_anim['sm'].append(img_sm)

player_img = pygame.image.load(path.join(img_dir, "spaceship1.png")).convert()
player_img1 = pygame.image.load(path.join(img_dir, "spaceship2.png")).convert()
player_img2 = pygame.image.load(path.join(img_dir, "spaceship3.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (45, 45))
player_mini_img.set_colorkey(BLACK)
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0
pygame.mixer.music.play(loops=-1)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Killer!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    if (firstPlay):
        draw_text(screen, "Arrow keys move, Space to fire", 22,
                  WIDTH / 2, HEIGHT / 2)
    else:
        draw_text(screen, "Your last score " + str(score), 18, WIDTH / 2, HEIGHT * 2 / 4)

    pygame.display.flip()
    waiting = True
    while waiting:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
# Цикл игры
game_over = True
running = True
firstPlay= True
while running:
    if game_over:
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
        firstPlay = False
        game_over = False
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)

    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    #  Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if 50 <= player.shield < 70:
            player.image = pygame.transform.scale(player_img1, (100, 100))
            player.image.set_colorkey(BLACK)
        if 0 < player.shield < 50:
            player.image = pygame.transform.scale(player_img2, (100, 100))
            player.image.set_colorkey(BLACK)
        if player.shield <= 0:
            expl_player = Explosion(player.rect.center, 'lg')
            all_sprites.add(expl_player)
            player.image = pygame.transform.scale(player_img, (100, 100))
            player.image.set_colorkey(BLACK)
            player.hide()
            player.lives -= 1
            player.shield = 100
        # Если игрок умер, игра окончена
        if player.lives == 0 and not expl_player.alive():
            game_over = True
    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        pow_sound.play()
        if hit.type == 'HP':
            player.shield += random.randrange(10, 30)
            if 50 <= player.shield < 70:
                player.image = pygame.transform.scale(player_img1, (100, 100))
                player.image.set_colorkey(BLACK)
            if 0 < player.shield < 50:
                player.image = pygame.transform.scale(player_img2, (100, 100))
                player.image.set_colorkey(BLACK)
            if player.shield >= 100:
                player.image = pygame.transform.scale(player_img, (100, 100))
                player.image.set_colorkey(BLACK)
                player.shield = 100
        if hit.type == 'bullet_upgrade':
            player.powerup()
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'SCORE '+str(score), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 100, 5, player.lives,player_mini_img)
    draw_shield_bar(screen, 5, 5, player.shield)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()