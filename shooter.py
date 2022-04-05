from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, width, height, speed = 0):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    def shoot(self):
        b = Bullet("bullet.png", x=0, y=0, width=15, height=20, speed=6)
        b.rect.centerx = self.rect.centerx
        b.rect.bottom = self.rect.top
        bullets.add(b)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > _HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, _WIDTH-self.rect.width)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > _HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, _WIDTH-self.rect.width)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

#region SETUP
_WIDTH = 800
_HEIGHT = 640

window = display.set_mode((_WIDTH, _HEIGHT))
clock = time.Clock()

background = GameSprite("galaxy.jpg", 0, 0, _WIDTH, _HEIGHT)
game_over = GameSprite("game-over.png", 0, 0, _WIDTH, _HEIGHT)
player = Player("rocket.png", _WIDTH/2, _HEIGHT-95, 60, 80, speed=10)
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()

def create_enemy():
    rand_speed = randint(1, 5)
    enemy = Enemy("ufo.png", x=0, y=0, width=80, height=60, speed=rand_speed)
    enemy.rect.x = randint(0, _WIDTH-enemy.rect.width)
    enemy.rect.bottom = 0
    enemies.add(enemy)

for i in range(6):
    create_enemy()

def create_asteroid():
    asteroid = Asteroid("ball.png", x=0, y=0, width=50, height=50, speed=1)
    asteroid.rect.x = randint(0, _WIDTH-asteroid.rect.width)
    asteroid.rect.bottom = 0
    asteroids.add(asteroid)

for i in range(2):
    create_asteroid()

font.init()
f = font.Font(None, 70)
points = 0

#endregion SETUP
death = False
destroyed = False
done = False
game_is_running = True
while game_is_running:
    for e in event.get():
        if e.type == QUIT:
            game_is_running = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            player.shoot()
 
    background.draw(window)
 
    if not death and not destroyed:
        enemies.update()
        enemies.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
    
        player.update()
        player.draw(window)

        points_image = f.render(str(points), True, (255, 255, 255))
        window.blit(points_image, (30, 30))

    hits = sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        create_enemy()
        points += 1
    
    sprite.groupcollide(asteroids, bullets, False, True)

    death = sprite.spritecollide(player, enemies, False)
    destroyed = sprite.spritecollide(player, asteroids, False)
    if death or destroyed:
        game_over.draw(window)

    display.update()
    clock.tick(60)
