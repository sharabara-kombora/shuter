#Создай собственный Шутер!

from pygame import *
mixer.init()
font.init()
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), player_size)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def sp(self):
        p = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, (15, 30))
        puli.add(p)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 570:
            global propusheno
            propusheno += 1
            self.rect.y = randint(-70, -50)
            self.rect.x = randint(0, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

schet = 0
propusheno = 0

mw = display.set_mode((700, 500))
display.set_caption('Шутер')
fon = transform.scale(image.load('galaxy.jpg'), (700, 500))

igra = True

clock = time.Clock()
FPS = 60

mixer.music.load('space.ogg')
udar = mixer.Sound('fire.ogg')
udar.set_volume(0.15)
mixer.music.set_volume(0.05)
mixer.music.play()

igrok = Player('rocket.png', 310, 400, 7, (80, 100))

puli = sprite.Group()
#ufo.png
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ghost_dead.png', randint(0, 500), randint(-70, -50), randint(1, 2), (70, 100))
    monsters.add(enemy)

ast = sprite.Group()
for i in range(2):
    enemy = Enemy('piranha_dead.png', randint(0, 500), randint(-70, -50), 1, (50, 70))
    ast.add(enemy)

l = 5

finish = False

font = font.SysFont('Arial ', 50)

while igra:
    for e in event.get():
        if e.type == QUIT:
            igra = False 
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish == False:
                igrok.sp()
                udar.play()
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish == True:
                finish = False
                igrok.rect.x = 310
                schet = 0
                propusheno = 0
                l = 5
                monsters = sprite.Group()
                for i in range(5):
                    enemy = Enemy('ghost_dead.png', randint(0, 500), randint(-70, -50), randint(1, 3), (70, 100))
                    monsters.add(enemy)
                ast = sprite.Group()
                for i in range(2):
                    enemy = Enemy('piranha_dead.png', randint(0, 500), randint(-70, -50), 1, (50, 70))
                    ast.add(enemy)
    mw.blit(fon, (0, 0)) 
    if finish == False:
        igrok.reset()
        igrok.update()
        monsters.draw(mw)
        monsters.update()
        ast.draw(mw)
        ast.update()
        puli.draw(mw)
        puli.update()
        sch = font.render('Счёт: '+ str(schet), True, (250, 250, 250))
        pr = font.render('Пропущено: '+ str(propusheno), True, (250, 250, 250))
        li = font.render(str(l), True, (250, 0, 0))
        mw.blit(sch, (5, 5))
        mw.blit(pr, (5, 50))
        mw.blit(li, (650, 5))
        ksi = sprite.spritecollide(igrok, monsters, True)
        kisa = sprite.spritecollide(igrok, ast, True)
        if kisa:
            l -= 1
            enemy = Enemy('piranha_dead.png', randint(0, 500), randint(-70, -50), randint(1, 3), (50, 70))
            ast.add(enemy)
        if ksi:
            l -= 1
            enemy = Enemy('ghost_dead.png', randint(0, 500), randint(-70, -50), randint(1, 3), (70, 100))
            monsters.add(enemy)
        if propusheno >= 10:
            finish = True
            winner = font.render('ВЫ ПРОИГРАЛИ ', True, (250, 250, 0))
        if schet >= 100:
            finish = True
            winner = font.render('ВЫ ВЫИГРАЛИ', True, (250, 250, 0))
        ksp = sprite.groupcollide(puli, monsters, True, True)
        if ksp:
            enemy = Enemy('ghost_dead.png', randint(0, 500), randint(-70, -50), randint(1, 3), (70, 100))
            monsters.add(enemy)
            schet += 1
        if l <= 0:
            finish = True
            winner = font.render('ВЫ ПРОИГРАЛИ ', True, (250, 250, 0))
    if finish:
        mw.blit(winner, (200, 200))
    clock.tick(FPS)
    display.update()