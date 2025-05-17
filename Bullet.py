import pygame
import math

from ObjectTopDown import ObjectTopDown


class Bullet(ObjectTopDown):
    def __init__(self, img, start_at, point_at, size=(2, 10), speed=9):
        ObjectTopDown.__init__(self, [img])

        self.rect.center = start_at
        self.speed = speed

        self.v = [0, 0]

        self.pointAt(point_at)

        self.frames_alive = 0
        self.lifetime_max = 1000


    def pointAt(self, point):
        dtheta = ObjectTopDown.pointAt(self, point)

        # also calc velocity
        vx = self.speed * math.cos(dtheta)
        vy = self.speed * math.sin(dtheta)
        self.v = [vx, -vy]


    def update(self, uvx, uvy):
        self.move(uvx + self.v[0], uvy + self.v[1])
        #self.move(self.v[0], self.v[1])

        self.frames_alive += 1
        if self.frames_alive > self.lifetime_max:
            self.kill()
