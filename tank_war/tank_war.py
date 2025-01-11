import pygame
import os
import random
FPS = 60
WIDTH = 1000
HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战")
clock = pygame.time.Clock()
running = True
expl_anim = {}
expl_anim['enemy'] = []
for i in range(5):
    expl_img  = pygame.image.load(os.path.join("img/explosion",f"expl{i}.png")).convert()
    expl_img.set_colorkey(WHITE)
    expl_anim['enemy'].append(pygame.transform.scale(expl_img,(75,75)))
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,type):
        super().__init__()
        self.type = type
        self.image = expl_anim[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.center  =center
        self.frame = 0
        self.last_update  =pygame.time.get_ticks()
        self.frame_rect = 58

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rect:
            self.frame += 1
            self.last_update = now
            if self.frame == len(expl_anim[self.type]):
                self.kill()
            else:
                self.image = expl_anim[self.type][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/myTank", "tank_T1_0.png")).convert()
        self.tank = tank_img
        self.tank.set_colorkey(WHITE)
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.direction = "UP"

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.tank.subsurface((0, 144), (48, 42))
            self.direction = "RIGHT"
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = self.tank.subsurface((0, 96), (48, 42))
            self.direction = "LEFT"
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            self.image = self.tank.subsurface((0, 0), (48, 48))
            self.direction = "UP"
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.image = self.tank.subsurface((0, 48), (48, 48))
            self.direction = "DOWN"
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        all_sprites.add(bullet)
        player_bullet_group.add(bullet)
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self,x) -> None:
        super().__init__()
        tank_img = pygame.image.load(os.path.join("img/enemyTank", "enemy_1_0.png")).convert()
        self.tank = tank_img
        self.tank.set_colorkey(WHITE)
        self.image = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.direction = "DOWN"

        if x is None:
            self.x = random.randint(0,2)
        else:
            self.x = x

        self.rect.left = self.x*300
        self.rect.top = 50

        self.step = 60

        self.cooling_time = 1000
        self.last_shoot_time = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if(now -self.last_shoot_time) < self.cooling_time:
            return
        bullet = Bullet(self.rect.centerx,self.rect.centery,self.direction)
        all_sprites.add(bullet)
        self.last_shoot_time  = now

    def rand_direction(self):
        num = random.randint(1, 4)
        if num == 1:
            return "UP"
        if num == 2:
            return "DOWN"
        if num == 3:
            return "LEFT"
        if num == 4:
            return "RIGHT"
    def move(self):
        if self.step <= 0:
            self.step = 60
            self.direction = self.rand_direction()
        if self.direction == "UP":
            self.image = self.tank.subsurface((0,0),(48,42))
            self.rect.y -= self.speed
        if self.direction == "DOWN":
            self.image = self.tank.subsurface((0,48),(48,42))
            self.rect.y += self.speed
        if self.direction == "LEFT":
            self.image = self.tank.subsurface((0,96),(48,42))
            self.rect.x -= self.speed
        if self.direction == "RIGHT":
            self.image = self.tank.subsurface((0,144),(48,42))
            self.rect.x += self.speed
        self.step -= 1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.shoot()
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction) -> None:
        super().__init__()
        self.bullets = [
            pygame.image.load('./img/bullet/bullet_up.png').convert(),
            pygame.image.load('./img/bullet/bullet_down.png').convert(),
            pygame.image.load('./img/bullet/bullet_left.png').convert(),
            pygame.image.load('./img/bullet/bullet_right.png').convert()
        ]
        for img in self.bullets:
            img.set_colorkey(WHITE)
        self.image = self.bullets[{"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}[direction]]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.direction = direction
    
    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed
        
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
all_sprites = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
player = Player()
enemy = EnemyTank(1)
all_sprites.add(player)
enemy_tank_group = pygame.sprite.Group()
for i in range(random.randint(5,20)):
    enemy = EnemyTank(i)
    all_sprites.add(enemy)
    enemy_tank_group.add(enemy)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    screen.fill(BLACK)
    all_sprites.update()
    hits_playbullet_enemytank = pygame.sprite.groupcollide(player_bullet_group,enemy_tank_group,True,True)
    for enemy in hits_playbullet_enemytank:
        expl = Explosion(enemy.rect.center,'enemy')
        all_sprites.add(expl)
    for enemy in enemy_tank_group:
        enemy.move()
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()