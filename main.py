#!/usr/bin/python3

import pygame, sys, random
from entity import *
pygame.init()

X = 900
Y = 600

BLACK = (0, 0, 0)
COLOR = (26, 0, 26)
MAGENTA = (0, 0, 0)

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("GhostPygame")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
pygame.mouse.set_visible(False)
pygame.display.toggle_fullscreen()

acc = 2

class Platform():
    def __init__(self, sizex, sizey, posx, posy, color):
        self.surf = pygame.surface.Surface((sizex, sizey))
        self.rect = self.surf.get_rect(midbottom=(posx, posy))
        self.surf.fill(color)

    def draw(self):
        screen.blit(self.surf, self.rect)

platforms = []
platforms.append(Platform(X, 5, X//2, Y, MAGENTA))
platforms.append(Platform(200, 5, 500, Y-185, COLOR))
platforms.append(Platform(200, 5, X, Y-95, COLOR))
platforms.append(Platform(200, 5, 200, Y-95, COLOR))
platforms.append(Platform(100, 5, 0, Y-140, COLOR))
platforms.append(Platform(200, 5, X, Y-275, COLOR))
platforms.append(Platform(200, 5, 150, Y-290, COLOR))
platforms.append(Platform(100, 5, 0, Y-480, COLOR))
platforms.append(Platform(100, 5, 500, Y-500, COLOR))
platforms.append(Platform(120, 5, X//2-50, Y-400, COLOR))
platforms.append(Platform(130, 5, X-150, Y-400, COLOR))
p_rects = [p.rect for p in platforms]

bg = GIFImage('assets/bg.gif')
end = GIFImage('assets/end.gif')
player1 = Bat()
player2 = Human()
enemy = Enemy()
fireball = Fireball(player2)

start = time.time()

while True:
    clock.tick(30)
    screen.fill(BLACK)
    bg.render(screen, (0,0))

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP8 and player2.on_ground(p_rects):
                    player2.jump = True
                if event.key == pygame.K_KP5:
                    fireball.launch(player2)
                if event.key == pygame.K_z and player1.rect.y > 0:
                    player1.jump = True
                if event.key == pygame.K_f:
                  pygame.display.toggle_fullscreen()
            elif event.type == pygame.USEREVENT + 1:
                enemy.timer = True

    player1.event(p_rects, enemy)
    player2.event(p_rects, enemy)
    player1.move(p_rects, screen)
    player2.move(p_rects, screen)
    player2.hit(player1, fireball)
    enemy.move(p_rects, player1, fireball)

    player1.draw(screen)
    player2.draw(screen)
    enemy.draw(screen)
    fireball.surf.render(screen, fireball.rect)
    for p in platforms:
      p.draw()

    if not player1.alive:
      screen.fill(BLACK)
      end.render(screen, (0,0))
      pygame.display.flip()
      print('The game\'s over')
      end = time.time()
      pygame.time.wait(5000)
      print('Closing tab...')
      temps = int(end - start) // 60
      print('The game was '+str(temps)+' minutes long.')
      sys.exit()

    pygame.display.flip()


