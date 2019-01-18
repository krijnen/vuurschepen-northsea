from math import *


class location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, v, theta):
        self.x += v * cos(theta / 180 * pi)
        self.y += v * sin(theta / 180 * pi)

    def distance(self, location):
        dx = location.x - self.x
        dy = location.y - self.y
        return sqrt(dx**2 + dy**2)

    def angle(self, location):
        dx = location.x - self.x
        dy = location.y - self.y
        return atan2(dx,dy)*180/pi
