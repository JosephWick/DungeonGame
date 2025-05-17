import pygame
import numpy as np

from ObjectTopDown import ObjectTopDown
from Bullet import Bullet


class Player(ObjectTopDown):

    def __init__(
        self, img_list, anim_int=4, speed=4, border=(1110, 1110), mvbox=(600, 800),
        dmg_amnt=10, shoot_freq=40
    ):
        super().__init__(img_list, anim_int)

        self.speed = speed
        self.ux = 0
        self.uy = 0

        self.borderx = border[0]
        self.bordery = border[1]

        self.mvboxX = mvbox[0]
        self.mvboxY = mvbox[1]

        # inventory type attributes
        self.max_health = 30
        self.current_health = 30
        self.gold = 0
        self.arrows = 10

        self.shoot_freq = shoot_freq
        self.arrow_cooldown = 0
        self.do_anim = False

        self.dmg_amnt = dmg_amnt


    def update(self):
        if self.do_anim:
            self.idle_animate()
            if self.image_idx == 0:
                self.do_anim = False

        mpos = pygame.mouse.get_pos()
        self.pointAt(mpos)

        if self.arrow_cooldown > 0:
            self.arrow_cooldown -= 1



    def move(self, up=False, down=False, left=False, right=False):
        vx = self.speed*right + -1*self.speed*left
        vy = -1*self.speed*up + self.speed*down

        # only move the actual image if we're close to the edge of the map
        self.ux += vx
        if abs(self.ux) < self.mvboxX:
            vx = 0
        if abs(self.ux) > self.borderx and np.sign(self.ux) == np.sign(vx):
            self.ux -= vx
            vx = 0
        # repeat for y
        self.uy += vy
        if abs(self.uy) < self.mvboxY:
            vy = 0
        if abs(self.uy) > self.bordery and np.sign(self.uy) == np.sign(vy):
            self.uy -= vy
            vy = 0

        self.rect = self.rect.move(vx, vy)
        

    def shoot(self, mouse_pos, image_bullet):
        if self.arrows > 0:
            new_bullet = Bullet(image_bullet, self.rect.center, mouse_pos)
            self.arrows -= 1
            self.arrow_cooldown = self.shoot_freq

            self.do_anim = True
            self.dt = self.anim_int - 1

            return new_bullet
        return None
