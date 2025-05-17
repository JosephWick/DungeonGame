import math
import pygame

class ObjectTopDown(pygame.sprite.Sprite):
    def __init__(self, img_list, anim_int=6):

        pygame.sprite.Sprite.__init__(self)

        self.image = img_list[0]
        self.image_list = img_list
        self.image_idx = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.anim_int = anim_int
        self.dt = 0

        # for rotations; sprite upward facing is 90
        self.corr_angle = 90
        self.angle = 0
    

    def move(self, vx, vy):
        self.rect = self.rect.move(vx, vy)
        self.mask = pygame.mask.from_surface(self.image)


    def pointAt(self, point):
        dx = point[0] - self.rect.centerx
        dy = point[1] - self.rect.centery
        dtheta = math.atan2(-dy, dx)

        self.angle = math.degrees(dtheta) - self.corr_angle

        self.image = pygame.transform.rotate(self.image_list[self.image_idx], self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)

        return dtheta


    def idle_animate(self):
        if self.anim_int < 0:
            return

        self.dt += 1
        if self.dt == self.anim_int:
            self.image_idx += 1
            if self.image_idx == len(self.image_list):
                self.image_idx = 0
            self.image = self.image_list[self.image_idx]
            self.dt = 0


    def update(self, uvx, uvy):
        self.move(uvx, uvy)
        self.idle_animate()
