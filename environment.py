import numpy as np
from math import *
import sailor
import location
import pygame
import sys
import boat


class environment(object):
    scale = (1280,760)
    def __init__(self):
        self.sailors = {boat.boat(): location.location(10, 10)}
        self.buoys = [location.location(10, 100)]
        self.wind = np.random.random() * 16 + 4
        self.direction = 0
        self.init_draw()

    def run(self):
        rudder = 0
        while 1:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print(event.type)
                    if(pygame.key.get_pressed()[pygame.K_DOWN] != 0) and rudder > -9:
                        rudder -= 1
                    if(pygame.key.get_pressed()[pygame.K_UP] != 0) and rudder < 9:
                        rudder += 1
            for sailer, loc in self.sailors.items():
                sailer.newwind(self.wind, self.direction)
                sailer.control(rudder, 1)
                sailer.update()
                loc.update(sailer.v, sailer.theta)
                boat45 = pygame.transform.rotate(self.boat45, sailer.theta)
                self.screen.blit(boat45, (640 - loc.y, 240 - loc.x))
                print(sailer.v, sailer.theta, rudder)
            pygame.display.update()
            pygame.time.delay(100)

    def init_draw(self):
        self.screen = pygame.display.set_mode(self.scale)
        self.boat45 = pygame.image.load('sb_45.jpg').convert()
        self.background = pygame.image.load('sea.jpg').convert()
        self.background = pygame.transform.scale(self.background, self.scale)
        self.screen.blit(self.background, (0, 0))


if __name__ == "__main__":
    e = environment()
    e.run()
