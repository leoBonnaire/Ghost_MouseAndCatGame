import pygame, sys, random
from GIFImage import *

print('Loading...')

X = 900
Y = 600
BatSpeed = 14
HumanSpeed = 16
EnemySpeed = [5,15]

acc = input('Choose the gravitational acceleration (in m/s²) : ')
acc = float(acc)
acc = acc/9.81 * 2
print('Opening game ...')

class Player():

  def move(self, p_rects, screen):

        if self.jump:
            self.y_speed = self.jumpHigh
            self.jump = False
        self.rect.bottom += self.y_speed

        if self.left and self.rect.left > 0:
          self.rect.centerx -= self.v
          self.orient = 'GAUCHE'
        if self.right and self.rect.right < X:
          self.rect.centerx += self.v
          self.orient = 'DROITE'

        if self.on_ground(p_rects):
            if self.y_speed >= 0:
                self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
                self.y_speed = 0
            else:
                self.rect.top = p_rects[self.rect.collidelist(p_rects)].bottom
                self.y_speed1 = 2
        else:
            self.y_speed += acc

  def on_ground(self, p_rects):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False

class Bat(Player):

  def __init__(self):
    self.jump = False
    self.left = False
    self.right = False
    self.orient = 'GAUCHE'
    self.y_speed = 0
    self.v = BatSpeed
    self.jumpHigh = -15
    self.surf = GIFImage('assets/bat.gif')
    self.rect = self.surf.get_rect()
    self.rect.x = X - self.surf.get_width() - 50
    self.rect.y = Y - self.surf.get_height()*2
    self.lives = 3
    self.heart = pygame.image.load('assets/heart.png').convert()
    self.heart.set_colorkey(self.heart.get_at((0,0)))
    self.alive = True

  def event(self, p_rects, enemy):
        self.left = False
        self.right = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.left = True
        if keys[pygame.K_d]:
            self.right = True

  def draw(self, screen):
        if self.orient == 'GAUCHE': self.surf.render(screen, self.rect)
        else: self.surf.render(screen, self.rect, True)
        for i in range(self.lives):
            screen.blit(self.heart, [i*20 + 20, 20])

class Human(Player):

  def __init__(self):
   self.jump = False
   self.left = False
   self.right = False
   self.orient = 'GAUCHE'
   self.y_speed = 0
   self.v = HumanSpeed
   self.jumpHigh = -17
   self.surf = GIFImage('assets/human.gif')
   self.rect = self.surf.get_rect()
   self.rect.y = Y/2

  def event(self, p_rects, enemy):
        self.left = False
        self.right = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP4]:
            self.left = True
        if keys[pygame.K_KP6]:
            self.right = True

  def hit(self, player, fire):
        if player.rect.colliderect(self.rect) or player.rect.colliderect(fire.rect):
            player.lives -= 1
            player.rect.midbottom = (0, 0)
        if player.lives == 0:
            player.alive = False

  def draw(self, screen):
      if self.orient == 'GAUCHE': self.surf.render(screen, self.rect)
      else: self.surf.render(screen, self.rect, True)

class Enemy(Player):
    def __init__(self):
        self.surf = GIFImage('assets/ghost.gif')
        self.rect = self.surf.get_rect()
        self.x_speed = random.randint(4, 8)
        self.y_speed = 0
        self.timer = False
        self.orient = 1

    def move(self, p_rects, player, fire):
        self.rect.centerx += self.x_speed
        if self.rect.left <= 0 or self.rect.right >= X:
            self.x_speed *= -1
            self.orient = not self.orient

        if self.on_ground(p_rects):
            self.rect.bottom = p_rects[self.rect.collidelist(p_rects)].top + 1
            self.y_speed = 0
        else:
            self.y_speed += acc
        self.rect.bottom += self.y_speed

        self.hit(player)

        if self.timer:
            self.timer = False
            fire.dispFire = False
            self.rect.midtop = (X//2, 0)
            self.x_speed = random.randint(EnemySpeed[0], EnemySpeed[1]) * ((self.x_speed > 0) - (self.x_speed < 0))

    def hit(self, player):
        if player.rect.colliderect(self.rect):
            player.lives -= 1
            player.rect.midbottom = (X//2, Y - 100)

    def draw(self, screen):
        if self.orient: self.surf.render(screen, self.rect)
        else: self.surf.render(screen, self.rect, True)

class Fireball():
  def __init__(self, human):
    self.surf = GIFImage('assets/fireball.gif')
    self.rect = self.surf.get_rect()
    self.rect.x = X
    self.rect.y = Y

  def launch(self, human):
    self.rect.x = human.rect.x + 10
    self.rect.y = human.rect.y - 150
    if human.orient == 'GAUCHE':
      self.rect.x -= (20 + self.surf.get_width())
    else:
      self.rect.x += 20
